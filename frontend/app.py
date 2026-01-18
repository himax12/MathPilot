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
        # Hot-fix for stale session state during development
        # Hot-fix for stale session state during development
        # If the existing memory object doesn't have the new method, force re-creation
        # Also force reload for OCR update (v8 fix: Transparency Safe Composite)
        if not hasattr(st.session_state.orchestrator.solver.memory, 'get_all_sessions') or not st.session_state.get('ocr_fix_applied_v8'):
            st.warning("⚠️ Updating system to new version (reloading OCR v8.0)...")
            
            # FORCE RELOAD of backend modules to pick up changes
            import importlib
            import backend.memory
            import backend.agents.solver
            import backend.orchestrator
            import backend.ocr
            
            importlib.reload(backend.memory)
            importlib.reload(backend.agents.solver)
            importlib.reload(backend.orchestrator)
            importlib.reload(backend.ocr)
            
            # Use the reloaded module to get the class, without shadowing the global 'Orchestrator' name
            st.session_state.orchestrator = backend.orchestrator.Orchestrator()
            st.session_state.ocr_fix_applied_v6 = True
            
            # Since we re-created the orchestrator, we should try to restore the session again
            if st.session_state.orchestrator.restore_session():
                 st.success("✅ Restored previous conversation (after update)!")
            st.rerun()

    # Normal initialization flow: Only restore if we JUST created the orchestrator
    # This prevents "New Chat" (which triggers rerun) from being overwritten by the old DB session
    if "orchestrator" not in st.session_state or not getattr(st.session_state, '_has_restored', False):
         if st.session_state.orchestrator.restore_session():
             st.success("✅ Restored previous conversation!")
         st.session_state._has_restored = True
    
    # Initialize deck generator
    if 'deck_generator' not in st.session_state:
        st.session_state.deck_generator = DeckGenerator(theme="dark")
    
    # Initialize messages list for frontend display
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sync backend memory to frontend state if frontend is empty but backend isn't
    # This handles the initial load from DB
    if not st.session_state.messages:
        backend_messages = st.session_state.orchestrator.solver.memory.messages
        for msg in backend_messages:
            deck_html = None
            if msg.deck:
                try:
                    deck_html = st.session_state.deck_generator.from_structured(msg.deck)
                except Exception:
                    pass
            
            st.session_state.messages.append({
                "role": msg.role,
                "content": msg.content,
                "deck_html": deck_html,
                "events": [] # Past events not persisted
            })
    
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
    
    # Custom CSS for ChatGPT-like feel
    st.markdown("""
    <style>
        /* Main Chat Area */
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .stChatMessage[data-testid="stChatMessageUser"] {
            background-color: #2b2b2b;
        }
        .stChatMessage[data-testid="stChatMessageAssistant"] {
            background-color: transparent;
        }
        
        /* Sidebar Styles */
        section[data-testid="stSidebar"] {
            background-color: #202123;
        }
        
        /* Input Styling */
        .stChatInput textarea {
            background-color: #40414f;
            color: white;
        }
        
        /* Font Tweak (Optional) */
        body {
            font-family: 'Söhne', 'ui-sans-serif', 'system-ui', -apple-system, 'Segoe UI', Roboto, Ubuntu, Cantarell, 'Noto Sans', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar with ChatGPT-style History
    with st.sidebar:
        # 1. New Chat Button (Top Priority)
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.orchestrator.clear_conversation()
            st.session_state.messages = []
            st.session_state.pending_input = None
            st.rerun()
            
        st.divider()
        
        # 2. History List
        st.subheader("🕒 History")
        
        # Fetch sessions directly from memory
        sessions = st.session_state.orchestrator.solver.memory.get_all_sessions()
        
        # Display sessions as buttons
        if not sessions:
            st.caption("No history yet.")
        
        # Display sessions with options
        for s in sessions:
            # Layout: Button (Left) + Options (Right)
            col1, col2 = st.columns([0.85, 0.15])
            
            # Data
            is_active = (s['session_id'] == st.session_state.orchestrator.solver.memory.session_id)
            title = s['title'] if s['title'] else f"Session {s['session_id'][:8]}"
            icon = "🟢" if is_active else "📄"
            label = f"{icon} {title}"
            
            with col1:
                if st.button(label, key=f"btn_{s['session_id']}", use_container_width=True):
                    if st.session_state.orchestrator.solver.memory.restore_session_by_id(s['session_id']):
                        st.session_state.messages = []
                        # Sync frontend
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
                                "events": []
                            })
                        st.rerun()
            
            with col2:
                # Per-session Options Popover
                with st.popover("⋮", use_container_width=True):
                    st.caption("Options")
                    
                    # Rename
                    new_name = st.text_input("Name", value=s['title'] or "", key=f"input_{s['session_id']}")
                    if st.button("Rename", key=f"ren_{s['session_id']}", use_container_width=True):
                        if new_name.strip():
                            st.session_state.orchestrator.solver.memory.update_title(new_name, s['session_id'])
                            st.rerun()
                    
                    st.divider()
                    
                    # Delete
                    if st.button("🗑️ Delete", key=f"del_{s['session_id']}", type="primary", use_container_width=True):
                        st.session_state.orchestrator.solver.memory.delete_session(s['session_id'])
                        st.rerun()

        st.divider()

        # 3. Input Options (Moved to bottom or collapsible)
        with st.expander("⚙️ Input Settings", expanded=False):
            input_mode = st.radio(
                "Input Method:",
                ["💬 Chat", "📷 Image Upload", "🎤 Audio Input"],
                index=0
            )

        if input_mode == "📷 Image Upload":
            st.caption("Upload Math Problem")
            from helper_inputs import handle_image_input
            extracted_text = handle_image_input()
            if extracted_text and st.button("✅ Solve Image", use_container_width=True):
                st.session_state.pending_input = extracted_text
                st.rerun()
        
        elif input_mode == "🎤 Audio Input":
            st.caption("Speak Your Problem")
            from helper_inputs import handle_audio_input
            transcribed_text = handle_audio_input()
            if transcribed_text and st.button("✅ Solve Audio", use_container_width=True):
                st.session_state.pending_input = transcribed_text
                st.rerun()
    
    # Process pending input from image/audio
    if st.session_state.pending_input:
        pending = st.session_state.pending_input
        st.session_state.pending_input = None
        process_input(pending)
        st.rerun() # Rerun to show the message
    
    # Display chat history
    try:
        for msg in st.session_state.messages:
            render_message(msg)
    except Exception as e:
        st.error(f"Error rendering conversation: {e}")
    
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
