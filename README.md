# Ultra Simple Financial RAG System

**GPU-optimized RAG for financial news - actually works!** 🚀

## Quick Start (3 steps)

1. **Install:**
```bash
pip install -r requirements.txt
```

2. **Test:**
```bash
python rag_system.py
```

3. **Use in your AI agent:**
```python
from rag_system import get_financial_context

# One line to get context
context = get_financial_context("Tesla earnings")
# Use context in your AI prompt
```

## That's it! ✅

## AI Agent Integration

### Method 1: Simple (recommended)
```python
from rag_system import get_financial_context

def my_ai_agent(question):
    context = get_financial_context(question)
    
    prompt = f"""
    Context: {context}
    Question: {question}
    Answer:"""
    
    return your_ai_model.generate(prompt)
```

### Method 2: Multiple queries
```python
from rag_system import create_rag_system

rag = create_rag_system()  # Create once

def my_ai_agent(question):
    context = rag.get_context(question)
    # Use context...
```

## Add Your Data

Just drop JSON files in `financial_data/`:

```json
{
  "title": "Company News",
  "content": "News content...",
  "company": "Company Name", 
  "date": "2024-01-01"
}
```

## Features

- ✅ **GPU Optimized**: Uses your RTX 3050 automatically
- ✅ **Actually Works**: No complex setup, no errors
- ✅ **Real-time**: Automatically loads new JSON files
- ✅ **Sample Data**: Creates test data automatically
- ✅ **One Function**: `get_financial_context(query)` - done!

## Test Everything

```bash
python test_rag.py
```

Shows exactly how to integrate with your AI agent.

---

**No Pathway complexity, no configuration files, no headaches - just works!** 🎯