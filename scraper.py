import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from time import sleep
from urllib.parse import urljoin
import re

class MoneyControlScraper:
    def __init__(self):
        self.base_url = "https://www.moneycontrol.com"
        self.news_url = "https://www.moneycontrol.com/news/business/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
    def create_folder(self):
        """Create a folder with current datetime"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"moneycontrol_news_{timestamp}"
        os.makedirs(folder_name, exist_ok=True)
        return folder_name
    
    def get_article_links(self, page_url):
        """Extract article links from the news page"""
        try:
            response = requests.get(page_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_links = set()
            
            # Find article links - MoneyControl uses specific classes
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Filter for news article URLs
                if '/news/' in href and href.startswith('http'):
                    article_links.add(href)
                elif href.startswith('/news/'):
                    article_links.add(urljoin(self.base_url, href))
            
            return list(article_links)
        
        except Exception as e:
            print(f"Error fetching article links: {e}")
            return []
    
    def scrape_article(self, url):
        """Scrape individual article content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_data = {
                'url': url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Extract title - multiple possible locations
            title_tag = (soup.find('h1', class_='article_title') or 
                        soup.find('h1', class_='artTitle') or
                        soup.find('h1') or
                        soup.find('title'))
            article_data['title'] = title_tag.get_text(strip=True) if title_tag else 'N/A'
            
            # Extract publish date - multiple possible locations
            date_tag = (soup.find('div', class_='article_schedule') or
                       soup.find('span', class_='article_schedule') or
                       soup.find('div', class_='arttidate') or
                       soup.find('time'))
            
            if date_tag:
                date_text = date_tag.get_text(strip=True)
                article_data['published_date'] = date_text
            else:
                article_data['published_date'] = 'N/A'
            
            # Extract author - multiple possible locations
            author_tag = (soup.find('div', class_='article_author') or
                         soup.find('span', class_='article_author') or
                         soup.find('a', class_='author') or
                         soup.find('div', class_='auther_name'))
            
            if author_tag:
                author_text = author_tag.get_text(strip=True)
                # Clean up author text
                author_text = re.sub(r'^By\s+', '', author_text, flags=re.IGNORECASE)
                article_data['author'] = author_text
            else:
                article_data['author'] = 'N/A'
            
            # Extract article content - try multiple selectors
            content_parts = []
            
            # Method 1: Look for main content wrapper
            content_div = (soup.find('div', class_='content_wrapper') or
                          soup.find('div', class_='article_desc') or
                          soup.find('div', class_='articleContent') or
                          soup.find('div', id='article_content') or
                          soup.find('article'))
            
            if content_div:
                # Remove script and style tags
                for script in content_div(['script', 'style', 'iframe']):
                    script.decompose()
                
                # Get all paragraphs
                paragraphs = content_div.find_all('p')
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:  # Filter out very short paragraphs
                        content_parts.append(text)
            
            # Method 2: If no content found, try finding all paragraphs in body
            if not content_parts:
                all_paragraphs = soup.find_all('p')
                for p in all_paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 30:
                        content_parts.append(text)
            
            article_data['content'] = '\n\n'.join(content_parts) if content_parts else 'N/A'
            article_data['content_length'] = len(article_data['content'])
            
            # Extract tags/categories
            tags = []
            
            # Try different tag selectors
            tag_containers = (soup.find('div', class_='article_tags') or
                            soup.find('div', class_='tags') or
                            soup.find('ul', class_='tags'))
            
            if tag_containers:
                tag_elements = tag_containers.find_all('a')
                for tag in tag_elements:
                    tag_text = tag.get_text(strip=True)
                    if tag_text:
                        tags.append(tag_text)
            
            # Also look for meta keywords
            meta_keywords = soup.find('meta', {'name': 'keywords'})
            if meta_keywords and meta_keywords.get('content'):
                keywords = meta_keywords['content'].split(',')
                tags.extend([k.strip() for k in keywords if k.strip()])
            
            article_data['tags'] = list(set(tags))  # Remove duplicates
            
            # Extract category from URL
            url_parts = url.split('/')
            if 'news' in url_parts:
                news_idx = url_parts.index('news')
                if news_idx + 1 < len(url_parts):
                    article_data['category'] = url_parts[news_idx + 1]
            
            return article_data
        
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_article(self, article_data, folder_name, index):
        """Save article as JSON file"""
        if article_data:
            # Create filename from title or use index
            title_slug = re.sub(r'[^\w\s-]', '', article_data['title'][:50])
            title_slug = re.sub(r'[-\s]+', '_', title_slug).strip('_')
            
            filename = f"article_{index:04d}_{title_slug}.json"
            filepath = os.path.join(folder_name, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(article_data, f, indent=2, ensure_ascii=False)
            
            content_preview = article_data['content'][:100] + "..." if len(article_data['content']) > 100 else article_data['content']
            print(f"Saved: {filename}")
            print(f"  Title: {article_data['title'][:60]}...")
            print(f"  Content length: {article_data['content_length']} chars")
            print(f"  Preview: {content_preview}")
    
    def run(self, max_articles=20, pages_to_scrape=1):
        """Main scraping function"""
        print("Starting MoneyControl News Scraper...")
        print("=" * 60)
        folder_name = self.create_folder()
        print(f"Created folder: {folder_name}\n")
        
        all_links = set()
        
        # Scrape multiple pages if needed
        for page in range(1, pages_to_scrape + 1):
            page_url = f"{self.news_url}page-{page}/" if page > 1 else self.news_url
            print(f"Fetching articles from page {page}...")
            links = self.get_article_links(page_url)
            all_links.update(links)
            print(f"  Found {len(links)} links on this page")
            sleep(1)  # Be polite to the server
        
        print(f"\nTotal unique article links found: {len(all_links)}")
        print("=" * 60)
        
        # Limit to max_articles
        links_to_scrape = list(all_links)[:max_articles]
        
        successful_scrapes = 0
        failed_scrapes = 0
        
        # Scrape each article
        for idx, link in enumerate(links_to_scrape, 1):
            print(f"\n[{idx}/{len(links_to_scrape)}] Scraping: {link}")
            article_data = self.scrape_article(link)
            
            if article_data and article_data['content'] != 'N/A':
                self.save_article(article_data, folder_name, idx)
                successful_scrapes += 1
            else:
                print(f"  ✗ Failed to scrape or no content found")
                failed_scrapes += 1
            
            sleep(2)  # Be polite - wait 2 seconds between requests
        
        # Create summary file
        summary = {
            'scrape_date': datetime.now().isoformat(),
            'total_articles_attempted': len(links_to_scrape),
            'successful_scrapes': successful_scrapes,
            'failed_scrapes': failed_scrapes,
            'folder': folder_name,
            'pages_scraped': pages_to_scrape
        }
        
        with open(os.path.join(folder_name, '_summary.json'), 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print("\n" + "=" * 60)
        print(f"✓ Scraping complete!")
        print(f"  Successful: {successful_scrapes}")
        print(f"  Failed: {failed_scrapes}")
        print(f"  Saved to: {folder_name}")
        print("=" * 60)

if __name__ == "__main__":
    scraper = MoneyControlScraper()
    
    # Scrape 20 articles from 2 pages
    # Adjust these parameters as needed
    scraper.run(max_articles=400, pages_to_scrape=100)