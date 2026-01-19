"""
Simple RAG System using Pathway - GPU Optimized
"""

import pathway as pw
import json
import torch
from pathlib import Path
from typing import List, Dict
import jsonlines

# Set Pathway license
pw.set_license_key("demo-license-key-with-telemetry")


class SimpleRAG:
    def __init__(self, data_dir: str = "moneycontrol_news"):
        self.data_dir = Path(data_dir)
        
        # Check if directory exists
        if not self.data_dir.exists():
            print(f"⚠️  Directory {self.data_dir} not found, using default financial_data")
            self.data_dir = Path("financial_data")
            self.data_dir.mkdir(exist_ok=True)
            self.create_sample_data()
        else:
            print(f"📂 Using data from: {self.data_dir}")
        
        # Use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Setup Pathway components
        self.setup_pathway_rag()
    
    def create_sample_data(self):
        """Create sample financial data in JSONL format for Pathway"""
        sample_data = [
            {
                "title": "Tesla Reports Strong Q4 Earnings",
                "content": "Tesla Inc. reported better-than-expected fourth-quarter earnings, with revenue reaching $25.2 billion. The electric vehicle maker delivered 484,507 vehicles in Q4, beating analyst estimates. CEO Elon Musk highlighted the company's progress in autonomous driving technology and energy storage solutions.",
                "company": "Tesla Inc.",
                "date": "2024-01-24"
            },
            {
                "title": "Apple's Services Revenue Hits Record High", 
                "content": "Apple Inc. announced record-breaking services revenue of $23.1 billion in the latest quarter. The growth was driven by App Store sales, iCloud subscriptions, and Apple Pay transactions. The company also reported strong iPhone sales despite market headwinds.",
                "company": "Apple Inc.",
                "date": "2024-01-25"
            },
            {
                "title": "Federal Reserve Signals Potential Rate Cuts",
                "content": "The Federal Reserve indicated it may consider interest rate cuts in 2024 if inflation continues to decline. Fed Chair Jerome Powell stated that the central bank is closely monitoring economic indicators and remains committed to achieving price stability.",
                "company": "Federal Reserve",
                "date": "2024-01-26"
            },
            {
                "title": "Microsoft Cloud Revenue Surges",
                "content": "Microsoft Corporation reported exceptional growth in its cloud computing division, with Azure revenue increasing by 30% year-over-year. The company's AI initiatives and enterprise solutions continue to drive strong demand.",
                "company": "Microsoft Corporation",
                "date": "2024-01-27"
            }
        ]
        
        # Save as JSONL for Pathway
        jsonl_path = self.data_dir / "financial_news.jsonl"
        with jsonlines.open(jsonl_path, mode='w') as writer:
            for item in sample_data:
                writer.write(item)
        
        print(f"Created {len(sample_data)} sample documents")
    
    def setup_pathway_rag(self):
        """Setup Pathway RAG pipeline"""
        
        # Define schema for financial news (supports both formats)
        class FinancialNewsSchema(pw.Schema):
            title: str
            content: str
            company: str
            date: str
            category: str
            author: str
        
        # Check if we have JSON files
        json_files = list(self.data_dir.glob("*.json"))
        
        if json_files:
            # Convert JSON files to JSONL for Pathway
            jsonl_path = self.data_dir / "_pathway_data.jsonl"
            
            with jsonlines.open(jsonl_path, mode='w') as writer:
                for json_file in json_files:
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                            
                            # Normalize the data structure
                            normalized = {
                                'title': data.get('title', ''),
                                'content': data.get('content', ''),
                                'company': data.get('company', ''),
                                'date': data.get('date', data.get('published_date', '')),
                                'category': data.get('category', ''),
                                'author': data.get('author', '')
                            }
                            writer.write(normalized)
                    except Exception as e:
                        print(f"Error processing {json_file}: {e}")
            
            print(f"✅ Converted {len(json_files)} JSON files to JSONL")
        
        # Read data with Pathway
        docs = pw.io.jsonlines.read(
            self.data_dir,
            schema=FinancialNewsSchema,
            mode="streaming"
        )
        
        # Combine text fields using UDF
        @pw.udf
        def combine_text(title: str, content: str, company: str, date: str, category: str) -> str:
            parts = [title]
            if content:
                parts.append(content)
            if company:
                parts.append(f"Company: {company}")
            if category:
                parts.append(f"Category: {category}")
            if date:
                parts.append(f"Date: {date}")
            return ". ".join(parts)
        
        # Create metadata UDF
        @pw.udf
        def create_metadata(title: str, company: str, date: str, category: str) -> dict:
            return {
                "title": title,
                "company": company,
                "date": date,
                "category": category
            }
        
        # Process documents - create 'data' and '_metadata' columns as Pathway expects
        processed = docs.select(
            data=combine_text(pw.this.title, pw.this.content, pw.this.company, pw.this.date, pw.this.category),
            _metadata=create_metadata(pw.this.title, pw.this.company, pw.this.date, pw.this.category)
        )
        
        # Setup embedder
        from pathway.xpacks.llm import embedders
        self.embedder = embedders.SentenceTransformerEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Setup vector store
        from pathway.xpacks.llm.vector_store import VectorStoreServer
        self.vector_store = VectorStoreServer(
            processed,
            embedder=self.embedder
        )
        
        print("✅ Pathway RAG pipeline ready!")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search using Pathway vector store"""
        # Note: Pathway's vector store works in streaming mode
        # For simple queries, we'll use the embedder directly
        results = []
        
        # This is a simplified search - in production you'd use Pathway's full capabilities
        print(f"Searching for: {query}")
        
        return results
    
    def get_context(self, query: str, max_length: int = 1000) -> str:
        """
        Get context for AI agent - uses semantic search on actual data
        
        Args:
            query: The query to search for
            max_length: Maximum length of context to return
            
        Returns:
            Formatted context string ready for AI prompt
        """
        try:
            # Use the embedder to search for similar content
            jsonl_path = self.data_dir / "_pathway_data.jsonl"
            
            if not jsonl_path.exists():
                return "No financial data available."
            
            # Load and search through the data
            import jsonlines
            from sentence_transformers import SentenceTransformer
            import numpy as np
            
            # Initialize embedder if not already done
            if not hasattr(self, '_search_model'):
                self._search_model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
            
            # Load documents
            documents = []
            with jsonlines.open(jsonl_path, 'r') as reader:
                for doc in reader:
                    documents.append(doc)
            
            if not documents:
                return "No financial documents found."
            
            # Create embeddings for documents if not cached
            if not hasattr(self, '_doc_embeddings') or len(self._doc_embeddings) != len(documents):
                print("🔍 Creating embeddings for search...")
                texts = [doc.get('content', '') + ' ' + doc.get('title', '') for doc in documents]
                self._doc_embeddings = self._search_model.encode(texts, convert_to_numpy=True)
                self._cached_docs = documents
                print(f"✅ Cached {len(documents)} document embeddings")
            
            # Encode query
            query_embedding = self._search_model.encode([query], convert_to_numpy=True)
            
            # Calculate similarities
            similarities = np.dot(self._doc_embeddings, query_embedding.T).flatten()
            
            # Get top 3 most similar documents
            top_indices = np.argsort(similarities)[::-1][:3]
            
            # Filter by minimum similarity threshold
            min_similarity = 0.1  # Adjust this threshold as needed
            relevant_docs = []
            
            for idx in top_indices:
                if similarities[idx] > min_similarity:
                    doc = self._cached_docs[idx]
                    relevant_docs.append({
                        'doc': doc,
                        'similarity': similarities[idx]
                    })
            
            if not relevant_docs:
                return "No relevant financial information found for your query."
            
            # Format context
            context_parts = ["Financial Context (via Semantic Search):"]
            current_length = len(context_parts[0])
            
            for i, item in enumerate(relevant_docs, 1):
                doc = item['doc']
                similarity = item['similarity']
                
                title = doc.get('title', 'Financial News')
                date = doc.get('date', 'Unknown date')
                company = doc.get('company', '')
                content = doc.get('content', '')
                
                # Create formatted entry
                entry = f"\n\n{i}. {title}"
                if date and date != 'Unknown date':
                    entry += f" ({date})"
                if company:
                    entry += f" - {company}"
                
                # Add content snippet (limit to avoid too long context)
                content_snippet = content[:400] + "..." if len(content) > 400 else content
                entry += f"\n{content_snippet}"
                entry += f"\n[Relevance: {similarity:.2f}]"
                
                # Check if adding this entry would exceed max length
                if current_length + len(entry) > max_length:
                    break
                
                context_parts.append(entry)
                current_length += len(entry)
            
            return "".join(context_parts)
            
        except Exception as e:
            print(f"Error in get_context: {e}")
            return f"Error retrieving context: {str(e)}"


# Simple global instance
_rag_instance = None

def get_financial_context(query: str) -> str:
    """Simple function to get financial context using Pathway"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = SimpleRAG()
    
    return _rag_instance.get_context(query)


def create_rag_system() -> SimpleRAG:
    """Create a RAG system instance with Pathway"""
    return SimpleRAG()


# Test
if __name__ == "__main__":
    print("🚀 Testing Pathway RAG System")
    print("=" * 40)
    
    rag = SimpleRAG()
    
    queries = [
        "Tesla earnings performance",
        "Apple revenue growth", 
        "Federal Reserve interest rates",
        "Microsoft cloud business"
    ]
    
    for query in queries:
        print(f"\n❓ Query: {query}")
        context = rag.get_context(query)
        print(f"📄 Context: {context[:200]}...")
    
    print("\n✅ Test completed!")