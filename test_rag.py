#!/usr/bin/env python3
"""
Test Ultra Simple RAG for AI Agent Integration
"""

from rag_system import get_financial_context, create_rag_system

def test_ai_agent_integration():
    """Test how to use RAG in an AI agent"""
    
    print("🤖 AI Agent Integration Test")
    print("=" * 40)
    
    # Method 1: Simple one-liner
    print("\n1️⃣ Simple one-liner usage:")
    context = get_financial_context("Tesla stock performance")
    print(f"Context: {context[:200]}...")
    
    # Method 2: Create instance for multiple queries
    print("\n2️⃣ Multiple queries with one instance:")
    rag = create_rag_system()
    
    queries = [
        "How is Tesla doing financially?",
        "What's Apple's latest performance?", 
        "Any Federal Reserve updates?",
        "Microsoft cloud growth?"
    ]
    
    for query in queries:
        context = rag.get_context(query)
        print(f"\n❓ Query: {query}")
        print(f"📄 Context: {context[:150]}...")
        
        # This is where you'd use the context in your AI prompt
        ai_prompt = f"""
You are a financial AI assistant. Use this context to answer the user's question.

Context: {context}

User Question: {query}

Answer:"""
        
        print(f"🤖 AI Prompt ready (length: {len(ai_prompt)} chars)")
    
    print("\n✅ AI Agent integration test completed!")

def example_ai_agent_function(user_question: str) -> str:
    """Example of how to integrate RAG in your AI agent"""
    
    # Get relevant financial context
    context = get_financial_context(user_question)
    
    # Create prompt for your AI model
    prompt = f"""
You are a helpful financial AI assistant. Use the provided context to answer questions about financial news and market information.

Context: {context}

User Question: {user_question}

Please provide a helpful and accurate response based on the context:
"""
    
    # Here you would call your AI model (OpenAI, Hugging Face, etc.)
    # response = your_ai_model.generate(prompt)
    
    # For demo, return the prompt
    return f"[AI would process this prompt of {len(prompt)} characters]"

if __name__ == "__main__":
    test_ai_agent_integration()
    
    print("\n" + "="*50)
    print("🎯 Example AI Agent Function:")
    
    example_response = example_ai_agent_function("What's Tesla's recent performance?")
    print(example_response)