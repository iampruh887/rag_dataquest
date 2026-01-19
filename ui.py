#!/usr/bin/env python3
"""
Working UI for Financial AI Agent - Gradio 6.x Compatible
"""

import gradio as gr
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Initialize components
print("🚀 Initializing Financial AI Agent...")

try:
    from gemini_agent import GeminiFinancialAgent
    agent = GeminiFinancialAgent()
    agent_ready = True
    print("✅ Gemini AI Ready")
except Exception as e:
    print(f"⚠️  Gemini not available: {e}")
    try:
        from rag_system import SimpleRAG
        rag = SimpleRAG(data_dir="moneycontrol_news")
        agent_ready = False
        print("✅ RAG-only mode ready")
    except Exception as e2:
        print(f"❌ RAG also failed: {e2}")
        agent_ready = False
        rag = None


def chat_function(message, history):
    """Chat function compatible with Gradio 6.x"""
    if not message.strip():
        return history, ""
    
    try:
        # Get response
        if agent_ready:
            response = agent.ask(message)
        elif rag:
            context = rag.get_context(message)
            response = f"**Financial Context:**\n\n{context[:800]}..."
        else:
            response = "❌ Neither Gemini nor RAG is available. Please check your setup."
        
        # Add to history in the new format
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ]
        
        return new_history, ""
        
    except Exception as e:
        error_response = f"❌ Error: {str(e)}"
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": error_response}
        ]
        return new_history, ""


def analyze_company(company_name):
    """Analyze company"""
    if not company_name.strip():
        return "Please enter a company name."
    
    try:
        if agent_ready:
            return agent.analyze_company(company_name)
        elif rag:
            context = rag.get_context(f"{company_name} analysis performance earnings")
            return f"**Analysis for {company_name}:**\n\n{context}"
        else:
            return "❌ Analysis not available. Please check your setup."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_market_summary():
    """Get market summary"""
    try:
        if agent_ready:
            return agent.market_summary()
        elif rag:
            context = rag.get_context("market trends analysis summary earnings reports")
            return f"**Market Summary:**\n\n{context}"
        else:
            return "❌ Market summary not available. Please check your setup."
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Create interface
with gr.Blocks(title="Financial AI Agent") as demo:
    
    # Header
    gr.HTML("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
            <h1>💼 Financial AI Agent</h1>
            <p>Powered by Pathway RAG + Google Gemini</p>
        </div>
    """)
    
    # Status
    status = "✅ Gemini AI Ready" if agent_ready else ("✅ RAG Only Mode" if rag else "❌ Setup Issues")
    gr.Markdown(f"**Status:** {status} | **Data:** moneycontrol_news (398 articles) | **GPU:** CUDA")
    
    with gr.Tabs():
        
        # Chat Tab
        with gr.Tab("💬 Chat"):
            gr.Markdown("### Ask questions about financial news")
            
            # Initialize chatbot with proper format
            chatbot = gr.Chatbot(
                value=[],  # Start with empty list
                height=500,
                label="Financial Assistant"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask about companies, markets, or financial news...",
                    label="Your Question",
                    scale=4
                )
                send_btn = gr.Button("Send 📤", variant="primary", scale=1)
            
            clear_btn = gr.Button("Clear Chat 🗑️")
            
            # Example questions
            gr.Markdown("### 💡 Example Questions")
            examples = [
                "What's the latest on Tech Mahindra?",
                "Tell me about recent earnings reports",
                "Any news about IT sector?",
                "What are the market trends?"
            ]
            
            for example in examples:
                gr.Markdown(f"💭 {example}")
            
            # Chat interactions
            send_btn.click(
                chat_function,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )
            
            msg.submit(
                chat_function,
                inputs=[msg, chatbot],
                outputs=[chatbot, msg]
            )
            
            clear_btn.click(
                lambda: ([], ""),
                outputs=[chatbot, msg]
            )
        
        # Analysis Tab
        with gr.Tab("📊 Company Analysis"):
            gr.Markdown("### Detailed Company Analysis")
            
            with gr.Row():
                company_input = gr.Textbox(
                    label="Company Name",
                    placeholder="e.g., Tech Mahindra, Apple, Tesla",
                    scale=3
                )
                analyze_btn = gr.Button("Analyze 🔍", variant="primary", scale=1)
            
            analysis_output = gr.Markdown(label="Analysis Results")
            
            analyze_btn.click(
                analyze_company,
                inputs=company_input,
                outputs=analysis_output
            )
            
            # Examples
            gr.Examples(
                examples=["Tech Mahindra", "Apple", "Tesla", "Microsoft"],
                inputs=company_input
            )
        
        # Market Summary Tab
        with gr.Tab("🌍 Market Summary"):
            gr.Markdown("### Overall Market Analysis")
            
            summary_btn = gr.Button("Get Market Summary 📈", variant="primary", size="lg")
            summary_output = gr.Markdown(label="Market Summary")
            
            summary_btn.click(
                get_market_summary,
                outputs=summary_output
            )
    
    # Footer
    gr.HTML("""
        <div style="text-align: center; padding: 20px; color: #666; border-top: 1px solid #eee; margin-top: 20px;">
            <p><strong>Financial AI Agent</strong> | Built with Pathway RAG + Google Gemini</p>
            <p style="font-size: 12px;">GPU-optimized for RTX 3050 | Real-time financial news analysis</p>
        </div>
    """)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Launching Financial AI Agent UI")
    print("="*60)
    print(f"Status: {status}")
    print("URL: http://localhost:7864")
    print("="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=False,
        show_error=True
    )