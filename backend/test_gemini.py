"""
Quick test script to verify Gemini API configuration and connectivity.
Run this before starting the full application.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_config():
    """Test Gemini configuration."""
    print("=" * 60)
    print("Gemini API Configuration Test")
    print("=" * 60)
    
    try:
        from app.config import settings
        
        print("\n✓ Configuration loaded successfully")
        print(f"  Provider: Google Gemini")
        print(f"  Model: {settings.gemini_model}")
        
        if not settings.gemini_api_key or settings.gemini_api_key == "your-gemini-key-here":
            print("\n✗ FAILED: Gemini API key not configured")
            return False
        
        print(f"  API Key: {settings.gemini_api_key[:20]}... (hidden)")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Configuration error: {str(e)}")
        return False


def test_gemini_connection():
    """Test Gemini API connection."""
    print("\n" + "-" * 60)
    print("Testing Gemini API Connection...")
    print("-" * 60)
    
    try:
        import google.generativeai as genai
        from app.config import settings
        
        # Configure Gemini
        genai.configure(api_key=settings.gemini_api_key)
        
        # Create model
        model = genai.GenerativeModel(settings.gemini_model)
        
        print(f"\n✓ Gemini model initialized: {settings.gemini_model}")
        
        # Test with simple prompt
        print("\nSending test prompt to Gemini...")
        response = model.generate_content("Say 'Hello, Blog Generator!' in JSON format with a 'message' key.")
        
        print(f"\n✓ API call successful!")
        print(f"  Response: {response.text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"\n✗ API connection error: {str(e)}")
        print("\nPossible issues:")
        print("  1. Invalid API key")
        print("  2. Network connectivity problem")
        print("  3. API quota exceeded")
        print("  4. Model name incorrect")
        return False


def test_blog_generator():
    """Test BlogGenerator class."""
    print("\n" + "-" * 60)
    print("Testing BlogGenerator Class...")
    print("-" * 60)
    
    try:
        from app.core.blog_generator import BlogGenerator
        
        generator = BlogGenerator()
        print(f"\n✓ BlogGenerator initialized")
        print(f"  Provider: {generator.provider}")
        print(f"  Model: {generator.model}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ BlogGenerator error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n🚀 Starting Gemini API Tests...\n")
    
    results = []
    
    # Test 1: Configuration
    results.append(("Configuration", test_gemini_config()))
    
    if results[0][1]:
        # Test 2: API Connection
        results.append(("API Connection", test_gemini_connection()))
        
        if results[1][1]:
            # Test 3: BlogGenerator
            results.append(("BlogGenerator Class", test_blog_generator()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Gemini API is ready to use.")
        print("\n🎉 You can now start the application:")
        print("   python -m uvicorn app.main:app --reload")
    else:
        print("⚠ Some tests failed. Please check the errors above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
