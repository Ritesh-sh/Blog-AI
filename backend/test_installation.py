"""
Simple test script to verify the installation and basic functionality.
Run this after installation to ensure everything is working.
"""

import sys


def test_imports():
    """Test if all required packages are installed."""
    print("Testing package imports...")
    
    try:
        import fastapi
        print("✓ FastAPI installed")
    except ImportError:
        print("✗ FastAPI not installed")
        return False
    
    try:
        import bs4
        print("✓ BeautifulSoup4 installed")
    except ImportError:
        print("✗ BeautifulSoup4 not installed")
        return False
    
    try:
        import keybert
        print("✓ KeyBERT installed")
    except ImportError:
        print("✗ KeyBERT not installed")
        return False
    
    try:
        import sentence_transformers
        print("✓ SentenceTransformers installed")
    except ImportError:
        print("✗ SentenceTransformers not installed")
        return False
    
    try:
        import gradio
        print("✓ Gradio installed")
    except ImportError:
        print("✗ Gradio not installed")
        return False
    
    return True


def test_config():
    """Test if configuration is set up."""
    print("\nTesting configuration...")
    
    try:
        from app.config import settings
        print("✓ Config loaded")
        
        if settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here":
            print("✓ Gemini API key configured")
        else:
            print("⚠ Gemini API key not configured (edit .env file)")
        
        print(f"✓ Gemini Model: {settings.gemini_model}")
        
        return True
    except Exception as e:
        print(f"✗ Config error: {str(e)}")
        return False


def test_models():
    """Test if NLP models can be loaded."""
    print("\nTesting NLP models...")
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Sentence Transformer model loaded")
        return True
    except Exception as e:
        print(f"⚠ Could not load model (will download on first use): {str(e)}")
        return True  # Not critical, will download on first use


def test_url_validator():
    """Test URL validator."""
    print("\nTesting URL validator...")
    
    try:
        from app.core.url_validator import validate_url
        
        # Test valid URL
        is_valid, error = validate_url("https://www.python.org")
        if is_valid:
            print("✓ URL validator working")
            return True
        else:
            print(f"⚠ URL validation returned: {error}")
            return True  # May fail due to network
    except Exception as e:
        print(f"✗ URL validator error: {str(e)}")
        return False


def test_basic_functionality():
    """Test basic module functionality."""
    print("\nTesting basic functionality...")
    
    try:
        from app.core.text_cleaner import clean_text
        
        test_text = "  This is a test!  https://example.com  "
        cleaned = clean_text(test_text)
        
        if cleaned:
            print("✓ Text cleaner working")
        else:
            print("✗ Text cleaner failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AI Blog Generator - Installation Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("NLP Models", test_models()))
    results.append(("URL Validator", test_url_validator()))
    results.append(("Basic Functionality", test_basic_functionality()))
    
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
        print("✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Make sure your API keys are configured in .env")
        print("2. Start the API: python -m uvicorn app.main:app --reload")
        print("3. Start the UI: python ui/gradio_app.py")
        print("4. Open http://localhost:7860 in your browser")
    else:
        print("⚠ Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Create .env file: copy .env.example .env")
        print("3. Add your API keys to .env")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
