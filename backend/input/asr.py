"""
MathASR - Audio Speech Recognition for Math Mentor.
Uses Google Cloud Speech-to-Text V2 (Chirp 2) for state-of-the-art accuracy.
"""

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from typing import Dict, Optional

from backend.config import config

class MathASR:
    """
    Handles audio input using Google STT V2 (Chirp model).
    
    Why Chirp?
    - Best-in-class accuracy for technical terms
    - Multlingual support
    - Robust to accents and noise
    """
    
    def __init__(self):
        """Initialize Google Speech Client."""
        if not config.GOOGLE_PROJECT_ID:
            # We allow initialization without creds to not crash app start,
            # but methods will fail if called.
            print("WARNING: GOOGLE_PROJECT_ID not set. ASR will not work.")
            self.client = None
            return
            
        try:
            self.client = SpeechClient()
            self.project_id = config.GOOGLE_PROJECT_ID
            # Use 'global' location for standard STT V2
            self.location = "global"
            
            # Use the default recognizer (underscore means default)
            self.recognizer_path = f"projects/{self.project_id}/locations/{self.location}/recognizers/_"
        except Exception as e:
            print(f"Failed to init Speech Client: {e}")
            self.client = None

    def transcribe(self, audio_bytes: bytes) -> Dict[str, any]:
        """
        Transcribe audio bytes to text.
        
        Args:
            audio_bytes: Raw audio content (WAV/MP3/WebM)
            
        Returns:
            Dict with:
            - 'text': Transcribed text
            - 'confidence': Confidence score
            - 'error': Error message if any
        """
        if not self.client:
            return {
                "text": "",
                "confidence": 0.0,
                "error": "ASR not configured (missing Project ID)"
            }
            
        try:
            # Build configuration - use auto-detect for audio format
            # Streamlit audio_input returns WebM/Opus format
            config_req = cloud_speech.RecognitionConfig(
                # Let the API auto-detect the audio encoding
                auto_decoding_config={},
                language_codes=["en-US"],
                model="long",
            )
            
            request = cloud_speech.RecognizeRequest(
                recognizer=self.recognizer_path,
                config=config_req,
                content=audio_bytes
            )
            
            # Call API
            response = self.client.recognize(request=request)
            
            # Parse response
            results = response.results
            if not results:
                return {"text": "", "confidence": 0.0, "error": "No speech detected"}
                
            # Combine all results
            full_transcript = ""
            total_confidence = 0.0
            
            for result in results:
                if result.alternatives:
                    alt = result.alternatives[0]
                    full_transcript += alt.transcript + " "
                    total_confidence += alt.confidence
            
            avg_confidence = total_confidence / len(results) if results else 0.0
            
            return {
                "text": full_transcript.strip(),
                "confidence": avg_confidence,
                "error": None
            }
            
        except Exception as e:
            return {
                "text": "",
                "confidence": 0.0,
                "error": str(e)
            }

if __name__ == "__main__":
    # Test initialization
    asr = MathASR()
    if asr.client:
        print(f"ASR Initialized for project: {config.GOOGLE_PROJECT_ID}")
    else:
        print("ASR Initialization failed (check config)")
