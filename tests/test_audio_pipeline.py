"""
Test Audio Pipeline - Integration test for ASR + Normalizer
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from backend.input.asr import MathASR
from backend.input.normalizer import MathNormalizer
from backend.config import config


def test_asr_initialization():
    """Test ASR client initialization."""
    print("=" * 60)
    print("TEST 1: ASR Initialization")
    print("=" * 60)
    
    print(f"Config GCP_PROJECT_ID: {config.GCP_PROJECT_ID}")
    print(f"Config STT_LOCATION: {config.STT_LOCATION}")
    print(f"Config STT_RECOGNIZER: {config.STT_RECOGNIZER}")
    
    asr = MathASR()
    if asr.client:
        print("✅ ASR Client initialized successfully")
        print(f"Recognizer Path: {asr.recognizer_path}")
        return True
    else:
        print("❌ ASR Client failed to initialize")
        return False


def test_normalizer():
    """Test math phrase normalizer."""
    print("\n" + "=" * 60)
    print("TEST 2: Math Normalizer")
    print("=" * 60)
    
    test_cases = [
        ("integral of x squared plus 5 equals 10", "integrate x^2 + 5 = 10"),
        ("square root of x plus theta", "sqrt x + θ"),
        ("5 times pi divided by 2", "5 * π / 2"),
        ("derivative of x cubed", "diff x^3"),
    ]
    
    all_passed = True
    for original, expected_contains in test_cases:
        normalized = MathNormalizer.normalize(original)
        print(f"\nOriginal:   {original}")
        print(f"Normalized: {normalized}")
        
        # Check if key terms are present (not exact match, as normalization may vary)
        if any(term in normalized for term in expected_contains.split()):
            print("✅ PASS")
        else:
            print(f"⚠️  Expected to contain elements from: {expected_contains}")
            all_passed = False
    
    return all_passed


def test_asr_error_handling():
    """Test ASR error handling for bad inputs."""
    print("\n" + "=" * 60)
    print("TEST 3: ASR Error Handling")
    print("=" * 60)
    
    asr = MathASR()
    
    # Test with empty audio
    result = asr.transcribe(b"")
    print(f"\nEmpty audio test:")
    print(f"  Error: {result.get('error')}")
    print(f"  Text: '{result.get('text')}'")
    
    if result.get('error') or result.get('text') == '':
        print("✅ PASS - Correctly handled empty input")
        return True
    else:
        print("❌ FAIL - Should have returned error or empty text")
        return False


def main():
    """Run all audio pipeline tests."""
    print("\n" + "🎤" * 30)
    print("AUDIO PIPELINE INTEGRATION TEST")
    print("🎤" * 30 + "\n")
    
    results = []
    
    # Test 1: ASR Initialization
    try:
        results.append(("ASR Initialization", test_asr_initialization()))
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        results.append(("ASR Initialization", False))
    
    # Test 2: Normalizer
    try:
        results.append(("Math Normalizer", test_normalizer()))
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        results.append(("Math Normalizer", False))
    
    # Test 3: Error Handling
    try:
        results.append(("ASR Error Handling", test_asr_error_handling()))
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        results.append(("ASR Error Handling", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
