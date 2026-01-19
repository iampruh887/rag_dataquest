#!/usr/bin/env python3
"""
Quick test for Gemini Financial Agent
"""

import os
from gemini_agent import GeminiFinancialAgent


def test_gemini_agent():
    """Test the Gemini agent with RAG"""
    
    print("🧪 Testing Gemini Financial Agent")
    print("="*50)
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n❌ GOOGLE_API_KEY not set!")
        print("\nTo test, set your API key:")
        print("  export GOOGLE_API_KEY='your-key-here'")
        print("\nOr add to .env file:")
        print("  GOOGLE_API_KEY=your-key-here")
        return
    
    try:
        # Initialize agent
        print("\n1️⃣ Initializing agent...")
        agent = GeminiFinancialAgent()
        
        # Test simple query
        print("\n2️⃣ Testing simple query...")
        print("-"*50)
        question = "How is Tesla performing?"
        print(f"❓ {question}")
        response = agent.ask(question)
        print(f"🤖 {response}")
        
        # Test without RAG
        print("\n3️⃣ Testing without RAG...")
        print("-"*50)
        question = "What do you know about Tesla?"
        print(f"❓ {question}")
        response = agent.ask(question, use_rag=False)
        print(f"🤖 {response}")
        
        # Test company analysis
        print("\n4️⃣ Testing company analysis...")
        print("-"*50)
        analysis = agent.analyze_company("Apple")
        print(f"🤖 {analysis}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_gemini_agent()