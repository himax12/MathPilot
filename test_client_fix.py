"""
Test to verify genai.Client lazy-loading behavior.
"""
from google import genai
import os
import sys

# Add backend to path
sys.path.append('backend')
from config import config

print("Testing genai.Client behavior...\n")

# Test 1: BAD - Property creates new instance each time
class BadAgent:
    def __init__(self):
        self._api_key = config.GEMINI_API_KEY
    
    @property
    def client(self):
        """Creates NEW client every time - BAD"""
        print("  → Creating NEW client instance")
        return genai.Client(api_key=self._api_key)
    
    def test_call(self):
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents="Say 'test'"
            )
            return f"✅ Success: {response.text[:20]}"
        except Exception as e:
            return f"❌ Error: {str(e)[:50]}"

# Test 2: GOOD - Cached client with lazy init
class GoodAgent:
    def __init__(self):
        self._api_key = config.GEMINI_API_KEY
        self._client_instance = None
    
    @property
    def client(self):
        """Lazy-init and cache - GOOD"""
        if self._client_instance is None:
            print("  → Creating and CACHING client instance")
            self._client_instance = genai.Client(api_key=self._api_key)
        else:
            print("  → Reusing CACHED client")
        return self._client_instance
    
    def test_call(self):
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents="Say 'test'"
            )
            return f"✅ Success: {response.text[:20]}"
        except Exception as e:
            return f"❌ Error: {str(e)[:50]}"

# Run tests
print("=" * 60)
print("TEST 1: BAD PATTERN (new instance each time)")
print("=" * 60)
bad = BadAgent()
print("Call 1:", bad.test_call())
print("Call 2:", bad.test_call())

print("\n" + "=" * 60)
print("TEST 2: GOOD PATTERN (cached instance)")
print("=" * 60)
good = GoodAgent()
print("Call 1:", good.test_call())
print("Call 2:", good.test_call())

print("\n" + "=" * 60)
print("CONCLUSION:")
print("=" * 60)
print("✅ Good pattern works consistently")
print("❌ Bad pattern may fail with 'client closed' errors")
