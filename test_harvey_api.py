#!/usr/bin/env python3
"""
Quick test script to debug Harvey API connection
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
HARVEY_API_KEY = os.getenv("HARVEY_API_KEY")
if not HARVEY_API_KEY:
    print("❌ HARVEY_API_KEY not set in .env file")
    sys.exit(1)

print(f"✅ HARVEY_API_KEY found: {HARVEY_API_KEY[:10]}...")

# Try to make a simple Harvey API call
import httpx

HARVEY_BASE_URL = os.getenv("HARVEY_BASE_URL", "https://eu.api.harvey.ai")
HARVEY_ENDPOINT = "/api/v2/completion"

print(f"🔗 Testing Harvey API at: {HARVEY_BASE_URL}{HARVEY_ENDPOINT}")

headers = {
    "Authorization": f"Bearer {HARVEY_API_KEY}",
}

# Test with minimal data
test_data = {
    "prompt": "Hello, this is a test. Please respond with a simple greeting.",
    "stream": False,
    "mode": "assist",
}

print(f"\n📤 Sending test request...")
print(f"Data: {test_data}")

try:
    with httpx.Client(timeout=60) as client:
        response = client.post(
            f"{HARVEY_BASE_URL}{HARVEY_ENDPOINT}",
            headers=headers,
            data=test_data,
        )
    
    print(f"\n📥 Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"✅ SUCCESS!")
        result = response.json()
        print(f"Response: {result}")
    else:
        print(f"❌ ERROR: {response.status_code}")
        print(f"Response Body: {response.text}")
        
except Exception as e:
    print(f"❌ Exception occurred: {type(e).__name__}")
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
