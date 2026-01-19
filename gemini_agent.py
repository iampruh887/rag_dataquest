#!/usr/bin/env python3
"""
Financial AI Agent using Google Gemini 2.5 with RAG
Powered by Google ADK (Agent Development Kit)
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rag_system import get_financial_context, create_rag_system

# Load environment variables
load_dotenv()


class GeminiFinancialAgent:
    """Financial AI Agent using Google Gemini 2.5 with RAG integration"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini agent with RAG
        
        Args:
            api_key: Google API key (or set GOOGLE_API_KEY env var)
        """
        # Get API key
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Please provide GOOGLE_API_KEY via parameter or environment variable")
        
        # Initialize Google ADK client
        self.client = genai.Client(api_key=self.api_key)
        
        # Initialize RAG system
        print("🔧 Initializing RAG system...")
        self.rag = create_rag_system()
        
        # Model configuration
        self.model_id = "gemini-2.5-flash"  # Using Gemini 1.5 Flash (more stable quota)
        
        print(f"✅ Gemini Financial Agent ready! Using model: {self.model_id}")
    
    def ask(self, question: str, use_rag: bool = True) -> str:
        """
        Ask the agent a financial question
        
        Args:
            question: User's question
            use_rag: Whether to use RAG for context (default: True)
            
        Returns:
            AI-generated answer
        """
        try:
            if use_rag:
                # Get relevant context from RAG
                context = self.rag.get_context(question)
                
                # Build prompt with context
                prompt = f"""You are a helpful financial AI assistant with access to recent financial news.

Financial News Context:
{context}

User Question: {question}

Please provide a clear, accurate answer based on the financial context above. If the context doesn't contain relevant information, say so."""
            else:
                # Ask without RAG context
                prompt = question
            
            # Generate response using Gemini
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    max_output_tokens=1024,
                )
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("💬 Gemini Financial Agent - Chat Mode")
        print("="*60)
        print("Ask me about financial news!")
        print("Commands: 'quit' to exit, 'norag' to disable RAG")
        print("-"*60)
        
        use_rag = True
        
        while True:
            try:
                question = input("\n🧑 You: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if question.lower() == 'norag':
                    use_rag = not use_rag
                    status = "enabled" if use_rag else "disabled"
                    print(f"🔧 RAG {status}")
                    continue
                
                print("🤖 Gemini: ", end="", flush=True)
                response = self.ask(question, use_rag=use_rag)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def analyze_company(self, company_name: str) -> str:
        """
        Get detailed analysis of a company
        
        Args:
            company_name: Name of the company
            
        Returns:
            Detailed analysis
        """
        question = f"Provide a detailed analysis of {company_name}'s recent performance, including financial metrics, market position, and outlook."
        return self.ask(question)
    
    def compare_companies(self, company1: str, company2: str) -> str:
        """
        Compare two companies
        
        Args:
            company1: First company name
            company2: Second company name
            
        Returns:
            Comparison analysis
        """
        question = f"Compare {company1} and {company2} based on recent financial news. Include performance metrics, market position, and growth prospects."
        return self.ask(question)
    
    def market_summary(self) -> str:
        """
        Get overall market summary
        
        Returns:
            Market summary
        """
        question = "Provide a summary of the current market conditions based on recent financial news. Include key trends, major company performances, and economic indicators."
        return self.ask(question)


def main():
    """Main function with examples"""
    
    print("="*60)
    print("🚀 Gemini Financial Agent with RAG")
    print("="*60)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n❌ Error: GOOGLE_API_KEY not found!")
        print("\nPlease set your Google API key:")
        print("  export GOOGLE_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("  GOOGLE_API_KEY=your-api-key-here")
        return
    
    try:
        # Initialize agent
        agent = GeminiFinancialAgent()
        
        # Example queries
        print("\n" + "="*60)
        print("📊 Example Queries")
        print("="*60)
        
        queries = [
            "How is Tesla performing financially?",
            "What's the latest on Apple's revenue?",
            "Any updates from the Federal Reserve?",
            "Tell me about Microsoft's cloud business"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\n{i}. ❓ {query}")
            print("-"*60)
            response = agent.ask(query)
            print(f"🤖 {response}")
        
        # Company analysis example
        print("\n" + "="*60)
        print("📈 Company Analysis Example")
        print("="*60)
        print("\n❓ Analyzing Tesla...")
        print("-"*60)
        analysis = agent.analyze_company("Tesla")
        print(f"🤖 {analysis}")
        
        # Market summary
        print("\n" + "="*60)
        print("🌍 Market Summary")
        print("="*60)
        summary = agent.market_summary()
        print(f"🤖 {summary}")
        
        # Interactive chat
        print("\n" + "="*60)
        print("💬 Starting Interactive Chat")
        print("="*60)
        agent.chat()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()