#!/usr/bin/env python3
"""
Test script to validate Harvey AI setup
Run this before starting the Django server to verify configuration
"""

import os
import sys

def test_environment_variables():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    harvey_key = os.environ.get("HARVEY_API_KEY")
    if not harvey_key:
        print("❌ HARVEY_API_KEY not set")
        print("   Fix: export HARVEY_API_KEY='your-key-here'")
        return False
    elif harvey_key == "your-harvey-api-key-here":
        print("❌ HARVEY_API_KEY still has placeholder value")
        print("   Fix: Set your actual Harvey API key")
        return False
    else:
        print(f"✅ HARVEY_API_KEY is set ({harvey_key[:10]}...)")
    
    base_url = os.environ.get("HARVEY_BASE_URL", "https://eu.api.harvey.ai")
    print(f"✅ HARVEY_BASE_URL: {base_url}")
    
    timeout = os.environ.get("HARVEY_TIMEOUT", "240")
    print(f"✅ HARVEY_TIMEOUT: {timeout} seconds")
    
    return True

def test_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ('httpx', 'httpx'),
        ('tenacity', 'tenacity'),
        ('django', 'Django'),
        ('openpyxl', 'openpyxl'),
    ]
    
    all_installed = True
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            print(f"❌ {package_name} not installed")
            all_installed = False
    
    if not all_installed:
        print("\n   Fix: pip install -r requirements.txt")
        return False
    
    return True

def test_harvey_config():
    """Test Harvey configuration import"""
    print("\n🔍 Testing Harvey configuration...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from core.harvey_agent.config import HARVEY_API_KEY, HARVEY_BASE_URL, HARVEY_TIMEOUT
        print(f"✅ Harvey config loaded successfully")
        print(f"   API Key: {HARVEY_API_KEY[:10]}...")
        print(f"   Base URL: {HARVEY_BASE_URL}")
        print(f"   Timeout: {HARVEY_TIMEOUT}s")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to load Harvey config: {e}")
        return False

def test_django_settings():
    """Test Django settings configuration"""
    print("\n🔍 Checking Django settings...")
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etf_ai_project.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        ai_provider = getattr(settings, 'AI_PROVIDER', 'not set')
        print(f"✅ AI_PROVIDER: {ai_provider}")
        
        if ai_provider.lower() == 'harvey':
            print("✅ Harvey AI is configured as the provider")
        elif ai_provider.lower() == 'openai':
            print("⚠️  OpenAI is configured as the provider")
            print("   To use Harvey, change AI_PROVIDER to 'harvey' in settings.py")
        else:
            print(f"⚠️  Unknown provider: {ai_provider}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to check Django settings: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Harvey AI Setup Validation")
    print("=" * 60)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Dependencies", test_dependencies),
        ("Harvey Configuration", test_harvey_config),
        ("Django Settings", test_django_settings),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! You're ready to use Harvey AI")
        print("=" * 60)
        print("\nNext steps:")
        print("1. python manage.py runserver")
        print("2. Upload an Excel file to test")
        print("3. Check logs for 'Using Harvey AI for text generation'")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("=" * 60)
        print("\nQuick fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set API key: export HARVEY_API_KEY='your-key'")
        print("3. Check settings.py: AI_PROVIDER = 'harvey'")
        return 1

if __name__ == "__main__":
    sys.exit(main())
