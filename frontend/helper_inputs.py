import streamlit as st
from PIL import Image
import io

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
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Initialize OCR if needed
        if st.session_state.ocr is None:
            try:
                with st.spinner("🔧 Initializing OCR..."):
                    from backend.ocr import MathOCR
                    st.session_state.ocr = MathOCR()
            except ValueError as e:
                st.error(f"❌ Configuration Error: {e}")
                st.info("💡 Please set GEMINI_API_KEY in your .env file")
                return None
        
        # Extract LaTeX
        with st.spinner("🔍 Extracting math expression..."):
            image_bytes_data = None
            
            # Smart-Pass: If image is reasonable size (< 4MB) and standard format, SEND AS IS.
            # This avoids PIL re-encoding corruption (e.g. contrast loss, transparency issues).
            if uploaded_file.size < 4 * 1024 * 1024:
                image_bytes_data = uploaded_file.getvalue()
                # Debug display
                with st.expander("🛠️ Debug: Raw Image Sent to AI", expanded=False):
                    st.image(image_bytes_data, caption="Bit-exact Raw Payload")
            else:
                # Resize if image is extremely large (max dimension 3072px) to prevent API errors
                # 3072px is plenty for OCR and keeps us well under 20MB limit
                image_bytes_io = io.BytesIO()
                max_dimension = 3072
                if max(image.size) > max_dimension:
                    ratio = max_dimension / max(image.size)
                    new_size = tuple(int(dim * ratio) for dim in image.size)
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
                    st.info(f"📏 Optimized image resolution to {new_size[0]}x{new_size[1]}")
                
                # Convert to RGB to ensure compatibility (remove alpha)
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')
                
                # Save as PNG (lossless) to preserve text details for OCR
                image.save(image_bytes_io, format='PNG')
                image_bytes_data = image_bytes_io.getvalue()

            ocr_result = st.session_state.ocr.extract_from_image(image_bytes_data)
        
        if ocr_result["error"]:
            st.error(f"❌ OCR Error: {ocr_result['error']}")
            return None
        
        # Display extracted expression (use expander to prevent overflow)
        st.markdown("**Extracted Expression**")
        if ocr_result["latex"] and not str(ocr_result["latex"]).startswith("UNCLEAR"):
            with st.expander("📄 View Full Extraction", expanded=True):
                st.markdown(ocr_result["latex"])
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
        
        return {
            "latex": edited_latex,
            "problem_data": ocr_result.get("problem_data", {})
        }
    return None

def handle_audio_input():
    """Handle audio recording and transcription."""
    st.markdown("### 🎙️ Audio Recorder")
    st.caption("Powered by Google Cloud Chirp 2 (State-of-the-art Speech Model)")
    
    # Initialize ASR
    if 'asr' not in st.session_state or st.session_state.asr is None:
        try:
            from backend.input.asr import MathASR
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
                    st.session_state.asr_confidence = 0.0
                else:
                    raw_text = result['text']
                    confidence = result.get('confidence', 0.0)
                    
                    st.success("Analysis Complete!")
                    
                    # Normalize
                    from backend.input.normalizer import MathNormalizer
                    normalized_text = MathNormalizer.normalize(raw_text)
                    
                    # Store in session state for persistence
                    st.session_state.transcribed_text = normalized_text
                    st.session_state.asr_confidence = confidence
        
        # Display the editable text area if we have transcription
        if st.session_state.get('transcribed_text'):
            conf = st.session_state.get('asr_confidence', 0.0)
            
            # Confidence warning
            if conf > 0 and conf < 0.85:
                st.warning(f"⚠️ Low confidence ({conf:.0%}). Please verify the transcription.")
            elif conf >= 0.85:
                st.success(f"✅ High confidence ({conf:.0%}).")
                
            edited_text = st.text_area(
                "Verify & Edit Transcription:",
                value=st.session_state.transcribed_text,
                height=100
            )
            
            # Update the stored text with any edits so it persists
            st.session_state.transcribed_text = edited_text
            
            return edited_text
            
        return None
    
    return None

