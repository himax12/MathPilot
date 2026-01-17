import streamlit as st
from PIL import Image
import io
import sys
import os

# Add backend to path to ensure imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

def handle_image_input():
    """Handle image upload and processing."""
    uploaded_file = st.file_uploader(
        "Upload an image of a math problem",
        type=["png", "jpg", "jpeg"],
        help="Take a clear photo of a printed or handwritten math problem"
    )
    
    if uploaded_file:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.session_state.current_image = image
        
        # Initialize OCR if needed
        if st.session_state.ocr is None:
            try:
                with st.spinner("🔧 Initializing OCR..."):
                    from input.ocr import MathOCR
                    st.session_state.ocr = MathOCR()
            except ValueError as e:
                st.error(f"❌ Configuration Error: {e}")
                st.info("💡 Please set GEMINI_API_KEY in your .env file")
                return None
        
        # Extract LaTeX
        with st.spinner("🔍 Extracting math expression..."):
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            ocr_result = st.session_state.ocr.extract_from_image(image_bytes.getvalue())
        
        if ocr_result["error"]:
            st.error(f"❌ OCR Error: {ocr_result['error']}")
            return None
        
        # Display extracted LaTeX
        st.markdown("**Extracted Expression**")
        if ocr_result["latex"] and not str(ocr_result["latex"]).startswith("UNCLEAR"):
            st.code(ocr_result["latex"])
        else:
            st.warning("⚠️ OCR unclear - manual input required")
            
        # HITL
        confidence = ocr_result["confidence"]
        if ocr_result["needs_review"]:
            st.warning(f"⚠️ Low confidence ({confidence:.0%}). Please verify.")
            
        edited_latex = st.text_area(
            "Verify & Edit:",
            value=ocr_result["latex"] if ocr_result["latex"] else "",
            height=100
        )
        
        return edited_latex
    return None

def handle_audio_input():
    """Handle audio recording and transcription."""
    st.markdown("### 🎙️ Audio Recorder")
    st.caption("Powered by Google Cloud Chirp 2 (State-of-the-art Speech Model)")
    
    # Initialize ASR
    if 'asr' not in st.session_state or st.session_state.asr is None:
        try:
            from input.asr import MathASR
            with st.spinner("🔧 Initializing Audio Engine..."):
                st.session_state.asr = MathASR()
        except ImportError:
            st.warning("⚠️ **Audio Input Not Available**")
            st.info("To enable audio input, install: `uv add google-cloud-speech`")
            return None
        except Exception as e:
            st.error(f"Failed to initialize ASR: {e}")
            return None


    # Audio Recorder
    audio_value = st.audio_input("Record your problem")
    
    if audio_value:
        st.audio(audio_value)
        
        if st.button("📝 Transcribe Audio"):
            with st.spinner("🎧 Transcribing with Chirp 2..."):
                raw_audio = audio_value.getvalue()
                result = st.session_state.asr.transcribe(raw_audio)
                
                if result['error']:
                    st.error(f"ASR Error: {result['error']}")
                    st.session_state.transcribed_text = None
                else:
                    raw_text = result['text']
                    
                    st.success("Analysis Complete!")
                    st.info(f"Transcript: {raw_text}")
                    
                    # Normalize
                    from input.normalizer import MathNormalizer
                    normalized_text = MathNormalizer.normalize(raw_text)
                    
                    st.markdown("**Normalized Math:**")
                    st.code(normalized_text)
                    
                    # Store in session state for persistence
                    st.session_state.transcribed_text = normalized_text
        
        # Return the persisted transcribed text
        return st.session_state.get('transcribed_text')
    
    return None

