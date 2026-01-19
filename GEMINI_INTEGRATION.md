# Gemini Financial Agent with RAG

Complete integration of Google Gemini 2.5 with Pathway RAG system for financial news analysis.

## Features

- ✅ **Google Gemini 2.5** - Latest AI model from Google
- ✅ **RAG Integration** - Pathway-powered context retrieval
- ✅ **GPU Optimized** - Fast embeddings on RTX 3050
- ✅ **Interactive Chat** - Real-time Q&A interface
- ✅ **Company Analysis** - Detailed financial analysis
- ✅ **Market Summaries** - Overall market insights

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy the key

### 3. Set API Key

**Option A: Environment Variable**
```bash
export GOOGLE_API_KEY='your-api-key-here'
```

**Option B: .env File**
```bash
cp .env.example .env
# Edit .env and add your key
```

## Quick Start

### Test the Agent

```bash
python test_gemini.py
```

### Interactive Chat

```bash
python gemini_agent.py
```

## Usage Examples

### Basic Usage

```python
from gemini_agent import GeminiFinancialAgent

# Initialize agent
agent = GeminiFinancialAgent()

# Ask a question
response = agent.ask("How is Tesla performing?")
print(response)
```

### Company Analysis

```python
# Detailed company analysis
analysis = agent.analyze_company("Tesla")
print(analysis)

# Compare companies
comparison = agent.compare_companies("Tesla", "Apple")
print(comparison)
```

### Market Summary

```python
# Get overall market summary
summary = agent.market_summary()
print(summary)
```

### Without RAG

```python
# Ask without RAG context (general knowledge only)
response = agent.ask("What is Tesla?", use_rag=False)
print(response)
```

### Interactive Chat

```python
# Start interactive chat mode
agent.chat()
```

Chat commands:
- Type your question to get an answer
- `norag` - Toggle RAG on/off
- `quit` - Exit chat

## How It Works

1. **User asks a question** → "How is Tesla performing?"

2. **RAG retrieves context** → Pathway searches financial news
   ```
   Context: Tesla Reports Strong Q4 Earnings...
   Revenue: $25.2 billion, Vehicles: 484,507...
   ```

3. **Gemini generates answer** → Using context + AI knowledge
   ```
   Tesla is performing strongly with Q4 earnings 
   beating expectations. Revenue reached $25.2B...
   ```

## Architecture

```
User Question
     ↓
RAG System (Pathway)
     ↓
Financial News Context
     ↓
Gemini 2.5 (Google ADK)
     ↓
AI-Generated Answer
```

## API Reference

### GeminiFinancialAgent

#### `__init__(api_key: str = None)`
Initialize the agent with optional API key.

#### `ask(question: str, use_rag: bool = True) -> str`
Ask a financial question.
- `question`: User's question
- `use_rag`: Whether to use RAG context (default: True)
- Returns: AI-generated answer

#### `analyze_company(company_name: str) -> str`
Get detailed analysis of a company.
- `company_name`: Name of the company
- Returns: Detailed analysis

#### `compare_companies(company1: str, company2: str) -> str`
Compare two companies.
- `company1`: First company name
- `company2`: Second company name
- Returns: Comparison analysis

#### `market_summary() -> str`
Get overall market summary.
- Returns: Market summary

#### `chat()`
Start interactive chat mode.

## Configuration

### Model Settings

Edit `gemini_agent.py` to customize:

```python
# Model ID
self.model_id = "gemini-2.0-flash-exp"

# Generation config
config=types.GenerateContentConfig(
    temperature=0.7,      # Creativity (0-1)
    top_p=0.95,          # Diversity
    max_output_tokens=1024,  # Max response length
)
```

### RAG Settings

Edit `rag_system.py` to customize:
- Embedding model
- Number of results
- Context length

## Adding Your Financial Data

Add JSONL files to `financial_data/`:

```jsonl
{"title": "Company Earnings", "content": "...", "company": "Company", "date": "2024-01-15"}
{"title": "Market Update", "content": "...", "company": "Market", "date": "2024-01-16"}
```

Pathway automatically detects and processes new files!

## Troubleshooting

### "GOOGLE_API_KEY not found"
- Set the environment variable or create .env file
- Get key from: https://aistudio.google.com/apikey

### "API quota exceeded"
- Check your Google Cloud quota
- Wait for quota reset or upgrade plan

### "CUDA not available"
- System will use CPU for embeddings
- Install CUDA toolkit for GPU acceleration

### "No relevant context found"
- Add more financial news to `financial_data/`
- Check that JSONL files are properly formatted

## Performance

- **RAG Search**: ~100ms (GPU) / ~500ms (CPU)
- **Gemini Response**: ~1-3 seconds
- **Total Response Time**: ~1-4 seconds

## Examples

### Example 1: Quick Question

```python
from gemini_agent import GeminiFinancialAgent

agent = GeminiFinancialAgent()
answer = agent.ask("What's Apple's latest revenue?")
print(answer)
```

Output:
```
Apple's services revenue hit a record high of $23.1 billion 
in the latest quarter, driven by App Store sales, iCloud 
subscriptions, and Apple Pay transactions...
```

### Example 2: Company Comparison

```python
comparison = agent.compare_companies("Tesla", "Apple")
print(comparison)
```

Output:
```
Tesla and Apple both showed strong performance:

Tesla: Q4 earnings of $25.2B, delivered 484,507 vehicles
Apple: Services revenue of $23.1B, strong iPhone sales

Tesla focuses on automotive/energy, while Apple dominates 
consumer tech and services...
```

### Example 3: Market Analysis

```python
summary = agent.market_summary()
print(summary)
```

Output:
```
Current market shows mixed signals:
- Tech sector: Strong with Apple and Microsoft growth
- Automotive: Tesla beating expectations
- Monetary policy: Fed considering rate cuts
Overall sentiment: Cautiously optimistic...
```

## Advanced Usage

### Custom Prompts

```python
agent = GeminiFinancialAgent()

# Get context manually
from rag_system import get_financial_context
context = get_financial_context("Tesla")

# Build custom prompt
custom_prompt = f"""
Analyze this financial data and provide investment advice:

{context}

Focus on: risk factors, growth potential, valuation
"""

response = agent.ask(custom_prompt, use_rag=False)
```

### Batch Processing

```python
agent = GeminiFinancialAgent()

companies = ["Tesla", "Apple", "Microsoft", "Amazon"]
analyses = {}

for company in companies:
    analyses[company] = agent.analyze_company(company)

# Save results
import json
with open("analyses.json", "w") as f:
    json.dump(analyses, f, indent=2)
```

## License

Open source - use freely in your projects.

## Support

For issues or questions:
1. Check this documentation
2. Review example code
3. Test with `test_gemini.py`

---

**Powered by Google Gemini 2.5 + Pathway RAG** 🚀