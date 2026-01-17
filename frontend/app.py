"""
Math Mentor - Chat-Based UI (Phase 4 Completed)
Conversational interface with SOTA Agentic Orchestrator.
"""

import streamlit as st
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import agents
try:
    from orchestrator import Orchestrator
    from deck_generator import DeckGenerator
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()




def init_session_state():
    """Initialize session state for chat mode."""
    # Initialize Orchestrator
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = Orchestrator()
    
    # Initialize deck generator
    if 'deck_generator' not in st.session_state:
        st.session_state.deck_generator = DeckGenerator(theme="dark")
    
    # Attempt to restore previous conversation
    if st.session_state.orchestrator.restore_session():
        st.success("✅ Restored previous conversation!")
    
    # Initialize messages list for frontend display
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history from memory
    messages = st.session_state.orchestrator.solver.memory.messages
    for msg in messages:
        with st.chat_message(msg.role):
            st.markdown(msg.content)
            if msg.deck:
                try:
                    deck_html = st.session_state.deck_generator.from_structured(msg.deck)
                    with st.expander("📊 Visual Explanation"):
                        st.components.v1.html(deck_html, height=600, scrolling=True)
                except Exception as e:
                    st.warning(f"Could not render deck: {e}")
    
    if 'ocr' not in st.session_state:
        st.session_state.ocr = None
    
    if 'pending_input' not in st.session_state:
        st.session_state.pending_input = None



def render_message(msg: dict):
    """Render a single chat message with optional deck."""
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    deck_html = msg.get("deck_html")
    events = msg.get("events", [])
    
    with st.chat_message(role):
        # Show thoughts/events if present (only for assistant)
        if role == "assistant" and events:
            with st.expander("🧠 Thinking Process", expanded=False):
                for event in events:
                    st.write(f"- {event}")
                    
        st.markdown(content)
        
        # Render deck if present
        if deck_html:
            with st.expander("📊 Visual Explanation", expanded=True):
                st.components.v1.html(deck_html, height=500, scrolling=True)


def process_input(user_input: str):
    """Process user input via Orchestrator."""
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Run Orchestrator
    with st.spinner("Thinking (Reflexion Architecture)..."):
        result = st.session_state.orchestrator.run(user_input)
    
    response_text = result.get("response", "")
    events = result.get("events", [])
    deck = result.get("deck")
    deck_html = None
    
    # Generate deck HTML if present
    if deck:
        try:
            deck_html = st.session_state.deck_generator.from_structured(deck)
        except Exception as e:
            st.error(f"Error rendering deck: {e}")
    
    # Store in history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "deck_html": deck_html,
        "events": events
    })


def main():
    st.set_page_config(
        page_title="Math Mentor",
        page_icon="🧮",
        layout="wide"
    )
    
    init_session_state()
    
    # Header
    st.title("🧮 Math Mentor")
    st.caption("Powered by Multi-Agent RAG & Reflexion")
    
    # Sidebar with multimodal input
    with st.sidebar:
        st.header("📥 Input Options")
        
        input_mode = st.radio(
            "Choose input method:",
            ["💬 Chat", "📷 Image Upload", "🎤 Audio Input"],
            horizontal=False
        )
        
        st.divider()
        
        if input_mode == "📷 Image Upload":
            st.subheader("📷 Upload Math Problem")
            from helper_inputs import handle_image_input
            extracted_text = handle_image_input()
            
            if extracted_text and st.button("✅ Use This Problem", use_container_width=True):
                st.session_state.pending_input = extracted_text
                st.rerun()
        
        elif input_mode == "🎤 Audio Input":
            st.subheader("🎤 Speak Your Problem")
            from helper_inputs import handle_audio_input
            transcribed_text = handle_audio_input()
            
            if transcribed_text and st.button("✅ Use This Problem", use_container_width=True):
                st.session_state.pending_input = transcribed_text
                st.rerun()
        
        st.divider()
        st.subheader("💾 Memory")
        if st.button("📂 Load Last Session", use_container_width=True):
            if st.session_state.orchestrator.solver.memory.restore_last_session():
                st.session_state.messages = []
                # Sync frontend state with backend memory
                for m in st.session_state.orchestrator.solver.memory.messages:
                    deck_html = None
                    if m.deck:
                        try:
                            deck_html = st.session_state.deck_generator.from_structured(m.deck)
                        except: pass
                    
                    st.session_state.messages.append({
                        "role": m.role,
                        "content": m.content,
                        "deck_html": deck_html,
                        "events": [] # Events not persisted
                    })
                st.success("History loaded!")
                st.rerun()
            else:
                st.warning("No previous session found.")

        st.divider()
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            # Reset orchestrator memory (via Solver)
            st.session_state.orchestrator.solver.reset_conversation()
            st.session_state.pending_input = None
            st.rerun()
        
        st.divider()
        st.markdown("**📚 Try asking:**")
        st.markdown("- Solve x² - 4 = 0")
        st.markdown("- Integrate sin(x) from 0 to pi")
        st.markdown("- Explain the concept of derivatives")
    
    # Process pending input from image/audio
    if st.session_state.pending_input:
        pending = st.session_state.pending_input
        st.session_state.pending_input = None
        process_input(pending)
        st.rerun() # Rerun to show the message
    
    # Display chat history
    for msg in st.session_state.messages:
        render_message(msg)
    
    # Chat input (always at bottom)
    if user_input := st.chat_input("Ask a math question..."):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing with Agents..."):
                result = st.session_state.orchestrator.run(user_input)
            
            response_text = result.get("response", "")
            events = result.get("events", [])
            deck = result.get("deck")
            deck_html = None
            
            # Show Thoughts
            if events:
                with st.expander("🧠 Thinking Process", expanded=True):
                    for event in events:
                        st.write(f"- {event}")
            
            # Show RAG Context explicitly
            ctx = result.get("context")
            if ctx and hasattr(ctx, "rag_context") and ctx.rag_context:
                with st.expander("📚 Knowledge Base Context", expanded=False):
                    st.markdown(f"```text\n{ctx.rag_context}\n```")

            # Render deck if present
            if deck:
                with st.spinner("Generating visual explanation..."):
                    try:
                        deck_html = st.session_state.deck_generator.from_structured(deck)
                    except Exception as e:
                        st.error(f"Deck error: {e}")
                
                st.markdown(response_text)
                with st.expander("📊 Visual Explanation", expanded=True):
                    st.components.v1.html(deck_html, height=500, scrolling=True)
            else:
                st.markdown(response_text)
            
            # Store in history
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "deck_html": deck_html,
                "events": events
            })


if __name__ == "__main__":
    main()
