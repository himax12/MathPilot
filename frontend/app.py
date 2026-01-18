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
    
    # Initialize deck generator (with reload check for new methods)
    if 'deck_generator' not in st.session_state:
        st.session_state.deck_generator = DeckGenerator(theme="dark")
    
    # Hot-fix: Check if deck_generator has new render_context method
    if not hasattr(st.session_state.deck_generator, 'render_context'):
        import importlib
        import backend.deck_generator.generator
        importlib.reload(backend.deck_generator.generator)
        from backend.deck_generator.generator import DeckGenerator as ReloadedDeckGenerator
        st.session_state.deck_generator = ReloadedDeckGenerator(theme="dark")
    
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



@st.dialog("📝 Provide Correct Answer")
def feedback_dialog(problem: str, wrong_answer: str):
    """Dialog for users to provide feedback on wrong answers."""
    st.caption("Help the AI learn from its mistake. This will be stored in memory.")
    
    st.text_area("Original Problem", value=problem, disabled=True, height=68)
    st.text_area("Wrong Answer", value=wrong_answer, disabled=True, height=68)
    
    correct_answer = st.text_input("Correct Answer", placeholder="e.g., 5.2 or x = 2")
    explanation = st.text_area("Explanation / Key Lesson", 
                              placeholder="Why is it wrong? e.g., 'You forgot to integrate the constant term'")
    
    if st.button("Submit Feedback", type="primary"):
        if correct_answer:
            with st.spinner("Saving to memory..."):
                # Call backend to store correction
                st.session_state.orchestrator.solver.memory.add_feedback(
                    problem=problem,
                    wrong_answer=wrong_answer,
                    correct_answer=correct_answer,
                    explanation=explanation
                )
            st.success("Feedback saved! I'll remember this next time.")
            import time
            time.sleep(1.5)
            st.rerun()
        else:
            st.warning("Please provide a correct answer.")

def render_message(msg: dict, msg_idx: int = 0):
    """Render a single chat message with enhanced metadata."""
    role = msg.get("role", "assistant")
    content = msg.get("content", "")
    deck_html = msg.get("deck_html")
    events = msg.get("events", [])
    confidence = msg.get("confidence")
    rag_context = msg.get("rag_context")
    solution_state = msg.get("solution_state") # Contains full context
    
    with st.chat_message(role):
        # 1. Main Content
        if deck_html:
            st.markdown(content)
            with st.expander("📊 Visual Explanation", expanded=True):
                st.components.v1.html(deck_html, height=500, scrolling=True)
        else:
            st.markdown(content)
            
        # 2. Metadata (Only for assistant)
        if role == "assistant":
            # Confidence Badge
            if confidence is not None and isinstance(confidence, (int, float)) and confidence > 0:
                color = "green" if confidence > 0.8 else "orange" if confidence > 0.5 else "red"
                st.caption(f"**Confidence:** :{color}[{confidence:.0%}]")

            # Agent Trace (What ran and why)
            if events:
                with st.expander("🕵️ Agent Trace", expanded=False):
                    for event in events:
                        st.write(f"- {event}")

            # Retrieved Context (Rendered as Deck)
            if rag_context:
                with st.expander("📚 Retrieved Context", expanded=False):
                    try:
                        context_html = st.session_state.deck_generator.render_context(rag_context)
                        st.components.v1.html(context_html, height=400, scrolling=True)
                    except Exception as e:
                        st.warning(f"Could not render context deck: {e}")
                        st.markdown(rag_context)

            # Feedback Buttons
            # Use message index for unique key
            col_fb1, col_fb2, _ = st.columns([0.1, 0.1, 0.8])
            with col_fb1:
                if st.button("✅", key=f"fb_pos_{msg_idx}", help="Correct"):
                    st.toast("Thanks for the feedback!", icon="👍")
            with col_fb2:
                if st.button("❌", key=f"fb_neg_{msg_idx}", help="Incorrect"):
                    # Get the problem context - ideally from solution_state or memory active_problem
                    # Fallback to current memory active problem if not available in msg
                    problem_context = st.session_state.orchestrator.solver.memory.active_problem or "Unknown Problem"
                    
                    # If solution_state is available, use exact values
                    ans_val = "See above"
                    if solution_state and hasattr(solution_state, 'answer'):
                         ans_val = str(solution_state.answer)
                    
                    feedback_dialog(problem_context, ans_val)


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
    confidence = result.get("confidence")
    rag_context = result.get("rag_context")
    
    deck_html = None
    
    # Generate deck HTML if present
    if deck:
        try:
            deck_html = st.session_state.deck_generator.from_structured(deck)
        except Exception as e:
            st.error(f"Error rendering deck: {e}")
    
    # Store in history
    import time
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "deck_html": deck_html,
        "events": events,
        "confidence": confidence,
        "rag_context": rag_context,
        "timestamp": time.time()
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
    
    # Custom CSS
    st.markdown("""
    <style>
        .stChatMessage { padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; }
        .stChatMessage[data-testid="stChatMessageUser"] { background-color: #2b2b2b; }
        .stChatMessage[data-testid="stChatMessageAssistant"] { background-color: transparent; }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar: History Only
    with st.sidebar:
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.orchestrator.clear_conversation()
            st.session_state.messages = []
            st.rerun()
            
        st.divider()
        st.subheader("🕒 History")
        
        sessions = st.session_state.orchestrator.solver.memory.get_all_sessions()
        if not sessions:
            st.caption("No history yet.")
            
        for s in sessions:
            col1, col2 = st.columns([0.85, 0.15])
            title = s['title'] if s['title'] else f"Session {s['session_id'][:8]}"
            is_active = (s['session_id'] == st.session_state.orchestrator.solver.memory.session_id)
            icon = "🟢" if is_active else "📄"
            
            with col1:
                if st.button(f"{icon} {title}", key=f"btn_{s['session_id']}", use_container_width=True):
                    if st.session_state.orchestrator.solver.memory.restore_session_by_id(s['session_id']):
                        st.session_state.messages = []
                        # Sync frontend
                        # NOTE: Historical messages might lack new metadata fields (confidence/rag), 
                        # so render_message must handle .get(None) gracefully.
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
                        st.rerun()
            
            with col2:
                with st.popover("⋮", use_container_width=True):
                    if st.button("🗑️", key=f"del_{s['session_id']}", type="primary"):
                        st.session_state.orchestrator.solver.memory.delete_session(s['session_id'])
                        st.rerun()

    # --- MAIN INPUT AREA (TABS) ---
    tab_chat, tab_image, tab_audio = st.tabs(["💬 Chat", "📷 Image", "🎤 Audio"])
    
    with tab_chat:
         st.caption("Type your math problem below.")
    
    with tab_image:
        from helper_inputs import handle_image_input
        extracted_text = handle_image_input()
        if extracted_text:
            if st.button("✅ Solve Extracted Problem", key="solve_img", type="primary"):
                process_input(extracted_text)
                st.rerun()

    with tab_audio:
        from helper_inputs import handle_audio_input
        transcribed_text = handle_audio_input()
        if transcribed_text:
            if st.button("✅ Solve Transcribed Problem", key="solve_audio", type="primary"):
                process_input(transcribed_text)
                st.rerun()

    st.divider()

    # Display Chat History
    try:
        for idx, msg in enumerate(st.session_state.messages):
            render_message(msg, idx)
    except Exception as e:
        st.error(f"Error rendering conversation: {e}")
    
    # Chat Input (Bottom) - Only active if using Chat Tab? 
    # Actually, standard UX is to have chat input available always or strictly within chat tab.
    # Given typical Streamlit layout, st.chat_input is fixed at bottom.
    # We will let it handle the "Chat" use case primarily.
    
    if user_input := st.chat_input("Ask a math question..."):
        process_input(user_input)
        st.rerun()

if __name__ == "__main__":
    main()
