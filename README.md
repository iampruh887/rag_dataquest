# **Gemini Financial Agent with Pathway RAG**

This documentation provides a technical overview and implementation guide for the **Gemini Financial Agent**, a high-performance system integrating **Google Gemini 2.5** with the **Pathway RAG** (Retrieval-Augmented Generation) framework. This architecture is designed for low-latency, context-aware financial news analysis and market synthesis.

## ---

**Core System Features**

* **Model Integration:** Powered by **Google Gemini 2.5**, optimized for deep financial reasoning and multimodal document understanding.  
* **Live RAG Pipeline:** Utilizes **Pathway** for real-time document indexing. Unlike static vector databases, Pathway automatically detects updates to your source files without requiring manual re-indexing.  
* **Hardware Acceleration:** Native support for **GPU-optimized embeddings** (specifically tuned for NVIDIA RTX 3050 and similar architectures) ensuring retrieval times under 100ms.  
* **Analysis Modules:** Specialized logic for **Company deep-dives**, **Comparative analysis**, and **Market sentiment summarization**.  
* **Dual-Interface Access:** Includes both a **Gradio-based Web UI** for visual dashboards and a **CLI** for rapid interactive sessions.

## ---

**Technical Architecture**

The system follows a linear retrieval-to-generation pipeline:

1. **Ingestion:** Pathway monitors the data directory (e.g., financial\_data/) for new or updated JSONL/JSON files.  
2. **Vector Retrieval:** User queries are converted into embeddings and matched against the live index.  
3. **Context Injection:** Relevant snippets are retrieved and injected into a structured system prompt.  
4. **Inference:** Gemini 2.5 processes the augmented prompt to generate a grounded response.

## ---

**Installation and Setup**

### **1\. Environment Configuration**

Ensure Python 3.10+ is installed. Clone the repository and install the core dependencies:

Bash

pip install \-r requirements.txt

### **2\. API Authentication**

Acquire a Google API Key from [Google AI Studio](https://aistudio.google.com/apikey).

**Method A: Environment Export**

Bash

export GOOGLE\_API\_KEY='your\_api\_key\_here'

Method B: Dotenv File  
Create a .env file in the root directory:

Plaintext

GOOGLE\_API\_KEY=your\_api\_key\_here

### **3\. Data Initialization**

Populate the financial\_data/ directory with news or reports. If starting from scratch, use the provided scraper:

Bash

python scraper.py

## ---

**Usage Guide**

### **Launching the Web Dashboard**

The Gradio UI provides separate tabs for chat, comparison, and market overviews.

Bash

python ui.py

**Default Access:** http://localhost:7864

### **Command Line Interface (CLI)**

Run the interactive agent directly in your terminal:

Bash

python gemini\_agent.py

* **norag**: Toggle to disable RAG and use Gemini's base training data only.  
* **quit**: Terminate the session.

## ---

**API Reference**

### **GeminiFinancialAgent Class**

The primary entry point for programmatic interaction.

| Method | Parameters | Description |
| :---- | :---- | :---- |
| **ask()** | question, use\_rag=True | General query function with optional context retrieval. |
| **analyze\_company()** | company\_name | Generates a structured SWOT or performance report. |
| **compare\_companies()** | c1, c2 | Side-by-side metric comparison and relative valuation. |
| **market\_summary()** | *None* | Aggregates all indexed news into a broad market outlook. |

## ---

**Configuration Details**

### **Model Parameters**

Modify gemini\_agent.py to adjust inference behavior:

* **temperature**: Set to **0.7** for a balance between factual accuracy and natural phrasing.  
* **top\_p**: Set to **0.95** to ensure diverse vocabulary in financial summaries.  
* **max\_output\_tokens**: Defaulted to **1024** for comprehensive multi-paragraph responses.

### **Pathway Optimization**

Pathway automatically utilizes CUDA if an NVIDIA GPU is detected. If the system logs **"CUDA not available"**, it will fall back to CPU-based indexing.

## ---

**Data Schema Requirements**

For optimal retrieval, ensure your financial data follows this JSON structure:

JSON

{  
  "title": "Quarterly Earnings Report",  
  "content": "Full text of the financial news or report here...",  
  "company": "NVIDIA",  
  "date": "2026-01-20",  
  "source": "Market News"  
}

---

**System powered by Google Gemini 2.5 \+ Pathway Streaming RAG.**
