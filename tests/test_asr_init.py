
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from backend.input.asr import MathASR
from backend.config import config

def test_init():
    print(f"Config GCP_PROJECT_ID: {config.GCP_PROJECT_ID}")
    print(f"Config STT_LOCATION: {config.STT_LOCATION}")
    print(f"Config STT_RECOGNIZER: {config.STT_RECOGNIZER}")
    
    asr = MathASR()
    if asr.client:
        print("✅ ASR Client initialized successfully")
        print(f"Recognizer Path: {asr.recognizer_path}")
    else:
        print("❌ ASR Client failed to initialize")

if __name__ == "__main__":
    test_init()
