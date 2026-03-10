#!/usr/bin/env python3
"""
Test script to verify API keys and basic functionality
"""

import os
from dotenv import load_dotenv
import openai

def test_environment_setup():
    """Test that .env file loads properly"""
    print("🔍 Testing environment setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if API keys are loaded
    openai_key = os.getenv('OPENAI_API_KEY')
    serper_key = os.getenv('SERPER_API_KEY')
    
    if openai_key:
        print(f"✅ OpenAI API Key loaded: {openai_key[:8]}...{openai_key[-4:]}")
    else:
        print("❌ OpenAI API Key not found in environment")
        return False
    
    if serper_key:
        print(f"✅ Serper API Key loaded: {serper_key[:8]}...{serper_key[-4:]}")
    else:
        print("⚠️  Serper API Key not found (optional)")
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI API connection...")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello, API test successful!'"}],
            max_tokens=50
        )
        
        message = response.choices[0].message.content
        print(f"✅ OpenAI API working: {message}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API test failed: {str(e)}")
        return False

def test_crewai_imports():
    """Test CrewAI imports"""
    print("\n🔍 Testing CrewAI imports...")
    
    try:
        from crewai import Agent, Task, Crew
        print("✅ CrewAI core imports successful")
        
        try:
            from crewai_tools import SerperDevTool, DuckDuckGoSearchRun
            print("✅ CrewAI tools imports successful")
        except ImportError as e:
            print(f"⚠️  Some CrewAI tools import failed: {e}")
            
        return True
        
    except ImportError as e:
        print(f"❌ CrewAI imports failed: {str(e)}")
        return False

def test_basic_agent_creation():
    """Test basic agent creation"""
    print("\n🔍 Testing basic agent creation...")
    
    try:
        from crewai import Agent
        
        agent = Agent(
            role="Test Agent",
            goal="Test the agent creation process",
            backstory="I am a test agent created to verify the setup works",
            verbose=True
        )
        
        print("✅ Basic agent creation successful")
        print(f"   Agent role: {agent.role}")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {str(e)}")
        return False

def test_web_scraping_tools():
    """Test web scraping functionality"""
    print("\n🔍 Testing web scraping tools...")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # Test basic web request
        response = requests.get("https://httpbin.org/html", timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup.find('h1'):
            print("✅ Web scraping tools working")
            return True
        else:
            print("⚠️  Web scraping partial success")
            return True
            
    except Exception as e:
        print(f"❌ Web scraping test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🚀 API Keys and Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("OpenAI Connection", test_openai_connection),
        ("CrewAI Imports", test_crewai_imports),
        ("Agent Creation", test_basic_agent_creation),
        ("Web Scraping", test_web_scraping_tools)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)