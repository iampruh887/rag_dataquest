# Financial RAG System with Pathway + Google Gemini 2.5

**GPU-optimized RAG using Pathway for financial news + Google Gemini 2.5 AI Agent** 🚀

Complete system for financial news analysis with:
- **Pathway** for real-time streaming data processing
- **Google Gemini 2.5** for intelligent AI responses
- **GPU acceleration** for fast embeddings (RTX 3050 optimized)

## Quick Start (3 steps)

1. **Install:**
```bash
pip install -r requirements.txt
```

1.2 **make knowledgebase**
```bash
python scraper.py
```

2. **Set Google API Key:**
```bash
export GOOGLE_API_KEY='your-api-key-here'
# Get key from: https://aistudio.google.com/apikey
```

3. **Launch UI:**
```bash
./start_ui.sh
# Or: python ui.py
```

Then open: **http://localhost:7864**

## Alternative: Command Line

```bash
# Test RAG system
python rag_system.py

# Test Gemini agent
python test_gemini.py

# Interactive chat
python gemini_agent.py
```

## Features

- ✅ **Beautiful Web UI**: Modern Gradio interface with multiple tabs
- ✅ **Pathway Powered**: Real-time streaming data processing
- ✅ **Gemini 2.5 AI**: Latest Google AI model integration
- ✅ **GPU Optimized**: Uses your RTX 3050 automatically
- ✅ **Interactive Chat**: Real-time Q&A with financial context
- ✅ **Company Analysis**: Detailed financial analysis tools
- ✅ **Auto-Updates**: Pathway monitors for new JSON files
- ✅ **MoneyControl Data**: Works with scraped financial news
- ✅ **Simple API**: One function call to get started

## UI Features

The web interface includes:

- 💬 **Chat Tab** - Interactive conversation with AI
- 📊 **Company Analysis** - Detailed company insights
- ⚖️ **Compare Companies** - Side-by-side comparison
- 🌍 **Market Summary** - Overall market analysis
- 🔍 **RAG Context Viewer** - See retrieved context

![UI Preview](https://via.placeholder.com/800x400?text=Financial+AI+Agent+UI)

## Usage Examples

### 1. Using Gemini AI Agent (Recommended)

```python
from gemini_agent import GeminiFinancialAgent

# Initialize agent
agent = GeminiFinancialAgent()

# Ask questions
response = agent.ask("How is Tesla performing?")
print(response)

# Company analysis
analysis = agent.analyze_company("Apple")
print(analysis)

# Interactive chat
agent.chat()
```

### 2. Using RAG Only (Custom AI Integration)

```python
from rag_system import get_financial_context

# Get context
context = get_financial_context("Tesla earnings")

# Use with your AI model
prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
response = your_ai_model.generate(prompt)
```

### 3. Multiple Queries

```python
from rag_system import create_rag_system

rag = create_rag_system()  # Create once

# Use many times
context1 = rag.get_context("Tesla")
context2 = rag.get_context("Apple")
```

## Add Your Financial Data

Drop JSONL files in `financial_data/`:

```jsonl
{"title": "Company News", "content": "News content...", "company": "Company Name", "date": "2024-01-01"}
{"title": "Market Update", "content": "More content...", "company": "Another Co", "date": "2024-01-02"}
```

Or JSON files (auto-converted):

```json
{
  "title": "Company News",
  "content": "News content...",
  "company": "Company Name", 
  "date": "2024-01-01"
}
```

Pathway automatically detects and processes new files!

## Documentation

- **[GEMINI_INTEGRATION.md](GEMINI_INTEGRATION.md)** - Complete Gemini integration guide
- **[README.md](README.md)** - This file with setup and usage instructions

## Data Source

The system uses the `moneycontrol_news` directory by default. This directory contains scraped financial news articles in JSON format.

**JSON Structure:**
```json
{
  "title": "Article Title",
  "content": "Full article content...",
  "published_date": "January 16, 2026",
  "author": "Author Name",
  "category": "business",
  "url": "https://..."
}
```

To use different data, change the directory in `ui.py` or `rag_system.py`.

## Test Everything

```bash
# Test RAG system
python test_rag.py

# Test Gemini agent
python test_gemini.py

# Run the UI
./start_ui.sh
```

---

**Powered by Pathway + Google Gemini 2.5 - Simple API, powerful AI!** 🎯