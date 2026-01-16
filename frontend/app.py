"""
Math Mentor - Complete Streamlit Frontend
Day 1: Text input → Answer
Day 2: Image OCR + Bidirectional Verification + HITL
"""

import streamlit as st
import sys
import os
from PIL import Image
import io

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from solver import SolverAgent
from executor import Executor
from ocr import MathOCR
from parser import ParserAgent


def init_session_state():
    """Initialize session state variables."""
    if 'solver' not in st.session_state:
        st.session_state.solver = None
    if 'executor' not in st.session_state:
        st.session_state.executor = Executor(timeout_seconds=5)
    if 'ocr' not in st.session_state:
        st.session_state.ocr = None
    if 'parser' not in st.session_state:
        st.session_state.parser = None
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'extracted_latex' not in st.session_state:
        st.session_state.extracted_latex = None
    if 'parsed_problem' not in st.session_state:
        st.session_state.parsed_problem = None


def display_header():
    """Display app header."""
    st.title("🧮 Math Mentor")
    st.markdown("**AI-powered math problem solver with OCR + Program-of-Thoughts**")
    st.markdown("---")


def display_examples():
    """Show example problems."""
    with st.expander("📚 Example Problems"):
        st.markdown("""
        **Algebra**:
        - Solve x² + 3x - 4 = 0 for x
        - Factor x² - 9
        - Simplify (x + 2)(x - 2)
        
        **Calculus**:
        - Integrate x² from 0 to 10
        - Find the derivative of sin(x) * cos(x)
        - Evaluate the limit of (x² - 1)/(x - 1) as x approaches 1
        
        **Probability**:
        - What is P(X < 2) where X ~ Normal(0, 1)?
        - Calculate the expected value of a fair six-sided die
        """)


def process_image_input(uploaded_file):
    """
    Process uploaded image: OCR → Bidirectional Verification → HITL
    
    This implements the "Vision-Parser Handover" pattern.
    """
    st.subheader("📷 Image Processing")
    
    # Display original image
    image = Image.open(uploaded_file)
    st.session_state.current_image = image
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Original Image**")
        st.image(image, width="stretch")
    
    # Initialize OCR if needed
    if st.session_state.ocr is None:
        try:
            with st.spinner("🔧 Initializing OCR..."):
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
    
    # Display extracted LaTeX (Bidirectional Verification)
    with col2:
        st.markdown("**Extracted Expression**")
        
        if ocr_result["latex"] and not ocr_result["latex"].startswith("UNCLEAR"):
            try:
                # Render LaTeX for visual comparison
                st.latex(ocr_result["latex"])
            except:
                st.code(ocr_result["latex"])
        else:
            st.warning("⚠️ OCR unclear - manual input required")
        
        # Show confidence
        confidence = ocr_result["confidence"]
        confidence_color = "green" if confidence >= 0.7 else "orange" if confidence >= 0.5 else "red"
        st.markdown(f"**Confidence:** :{confidence_color}[{confidence:.0%}]")
    
    # HITL: Allow user to edit extracted LaTeX
    st.markdown("---")
    st.subheader("✏️ Verify & Edit")
    
    # Pre-fill with extracted latex or empty if unclear
    default_latex = ocr_result["latex"] if not ocr_result["latex"].startswith("UNCLEAR") else ""
    
    edited_latex = st.text_area(
        "Extracted LaTeX (edit if needed):",
        value=default_latex,
        height=100,
        help="Verify the extracted expression is correct. Edit if needed."
    )
    
    # HITL warning for low confidence
    if ocr_result["needs_review"]:
        st.warning(f"⚠️ **HITL Triggered**: Confidence below threshold ({confidence:.0%} < 70%)")
        st.info("👁️ Please verify the extracted expression matches the image above")
    
    # Validate LaTeX syntax
    if edited_latex.strip():
        try:
            # Try to render it
            with st.expander("🔎 Preview Rendered LaTeX"):
                st.latex(edited_latex)
            
            # Basic validation: try parsing with sympy
            from sympy.parsing.latex import parse_latex
            try:
                parse_latex(edited_latex)
                st.success("✅ Valid LaTeX syntax")
            except:
                st.warning("⚠️ LaTeX might have syntax issues, but we'll try to solve it")
        except:
            pass
    
    st.session_state.extracted_latex = edited_latex
    
    # NEW: Parse the problem to understand it
    st.markdown("---")
    st.subheader("🧠 Problem Understanding")
    
    # Initialize parser if needed
    if st.session_state.parser is None:
        try:
            with st.spinner("🔧 Initializing Parser..."):
                st.session_state.parser = ParserAgent()
        except ValueError as e:
            st.error(f"❌ Configuration Error: {e}")
            return edited_latex  # Fallback: skip parsing
    
    # Parse the OCR output
    with st.spinner("🤔 Understanding the problem..."):
        parsed = st.session_state.parser.parse(ocr_result)
        st.session_state.parsed_problem = parsed
    
    if parsed["error"]:
        st.warning(f"⚠️ Parsing issue: {parsed['error']}")
        st.info("Will proceed with basic solving...")
    else:
        # Display parsed understanding
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**Question:**")
            st.info(parsed["question"])
            
            st.markdown("**Domain:**")
            st.success(f"📚 {parsed['domain'].title()}")
        
        with col_b:
            st.markdown("**Given Values:**")
            if parsed["given"]:
                for key, val in parsed["given"].items():
                    st.text(f"• {key} = {val}")
            else:
                st.text("None explicitly listed")
            
            st.markdown("**Approach:**")
            st.text(parsed["approach"] if parsed["approach"] else "Auto-determine")
        
        #Show confidence
        parse_conf = parsed["confidence"]
        conf_color = "green" if parse_conf >= 0.7 else "orange" if parse_conf >= 0.5 else "red"
        st.markdown(f"**Parser Confidence:** :{conf_color}[{parse_conf:.0%}]")
        
        # Show relationships if any
        if parsed.get("relationships"):
            with st.expander("📐 Relevant Formulas"):
                for rel in parsed["relationships"]:
                    st.markdown(f"- {rel}")
    
    return edited_latex


def solve_problem(problem: str, source: str = "text"):
    """
    Main solving pipeline: Problem → Solver → Executor → Answer
    """
    # Initialize solver if needed
    if st.session_state.solver is None:
        try:
            st.session_state.solver = SolverAgent()
        except ValueError as e:
            st.error(f"❌ Configuration Error: {e}")
            st.info("💡 Please set GEMINI_API_KEY in your .env file")
            return None
    
    # Step 1: Generate code (use parsed input if available)
    with st.spinner("🤔 Generating solution strategy..."):
        # Check if we have parsed problem data
        if hasattr(st.session_state, 'parsed_problem') and st.session_state.parsed_problem and not st.session_state.parsed_problem.get("error"):
            # Use context-aware solving
            solver_result = st.session_state.solver.solve_from_parsed(st.session_state.parsed_problem)
        else:
            # Fallback to basic solving
            solver_result = st.session_state.solver.solve(problem)
    
    if solver_result["error"]:
        st.error(f"❌ Solver Error: {solver_result['error']}")
        return None
    
    code = solver_result["code"]
    reasoning_text = solver_result["reasoning"]
    
    # Parse output
    reasoning = ""
    answer_interpretation = ""
    
    if reasoning_text:
        # Extract REASONING section
        if "**REASONING**" in reasoning_text:
                # Extract reasoning but remove the next section header if it exists
                raw_reasoning = parts[1].strip()
                # Split on various code section headers to be safe
                # IMPORTANT: Order matters. We splits on the first one we find to ensure clean cut.
                # User requested to KEEP visualization text but REMOVE calculation code.
                stop_markers = ["**CODE**", "CODE (calculation)", "CODE:"]
                for splitter in stop_markers:
                    if splitter in raw_reasoning:
                        raw_reasoning = raw_reasoning.split(splitter)[0]
                reasoning = raw_reasoning.strip()
        
        # Extract ANSWER section
        if "**ANSWER**" in reasoning_text:
            parts = reasoning_text.split("**ANSWER**")
            if len(parts) > 1:
                answer_interpretation = parts[1].strip().replace(":", "").strip()
    
    # Display verbose reasoning (Interactive Mode)
    if reasoning:
        st.subheader("🧠 Reasoning Process")
        
        # Try to parse properties
        intuition = ""
        steps_text = ""
        viz_plan = ""
        
        # 1. Extract Intuition
        if "**INTUITION**" in reasoning:
            parts = reasoning.split("**INTUITION**")
            if len(parts) > 1:
                content = parts[1]
                # Stop at next section
                if "**SOLUTION STEPS**" in content:
                    intuition = content.split("**SOLUTION STEPS**")[0].strip(" :*")
                else:
                    intuition = content.strip()
        
        # 2. Extract Steps
        if "**SOLUTION STEPS**" in reasoning:
            parts = reasoning.split("**SOLUTION STEPS**")
            if len(parts) > 1:
                content = parts[1]
                # Stop at visualization if present
                if "**VISUALIZATION**" in content:
                    steps_text = content.split("**VISUALIZATION**")[0].strip()
                    viz_plan = content.split("**VISUALIZATION**")[1].strip(" :*")
                else:
                    steps_text = content.strip()
        
        # Display Interactive Elements
        if intuition:
            with st.expander("💡 **Intuition**", expanded=True):
                st.info(intuition)
        
        if steps_text:
            st.markdown("### 📝 Steps")
            # Try to split by "**Step" to make individual expanders
            if "**Step" in steps_text:
                step_parts = steps_text.split("**Step")
                for part in step_parts:
                    if not part.strip(): continue
                    
                    # Reconstruct step title
                    # part usually looks like " 1**: Do this\n- details"
                    step_title = f"Step {part.split('**')[0].strip()}" if "**" in part else "Step"
                    step_body = part.split('**')[1].strip() if "**" in part else part
                    
                    # Clean up leading colon if present
                    if step_body.startswith(":"): step_body = step_body[1:].strip()
                    
                    with st.expander(f"📍 {step_title}", expanded=False):
                        st.markdown(step_body)
            else:
                # Fallback if specific formatting isn't found
                st.markdown(steps_text)
                
        if viz_plan:
            with st.expander("🎨 **Visualization Strategy**", expanded=False):
                st.markdown(viz_plan)
        
        # Fallback for unparsed reasoning
        if not intuition and not steps_text:
            st.markdown(reasoning)
            
        st.markdown("---")
    
    # Check for generated visualizations
    import os
    import glob
    plot_files = glob.glob("*.png") + glob.glob("explanation*.png")
    if plot_files:
        st.subheader("📊 Visual Explanation")
        for plot_file in plot_files[:3]:  # Show max 3 plots
            if os.path.exists(plot_file):
                st.image(plot_file, width="stretch")
                # Clean up after displaying
                try:
                    os.remove(plot_file)
                except:
                    pass
        st.markdown("---")
    
    # Code is completely hidden - users see reasoning + viz + answer only
    
    # Fallback: show raw reasoning if parsing failed
    if reasoning_text and not reasoning:
        with st.expander("💭 Raw Output"):
            st.markdown(reasoning_text)
    
    # Step 2: Execute code
    with st.spinner("⚙️ Executing code..."):
        exec_result = st.session_state.executor.execute(code)
    
    # Display execution results
    st.subheader("🎯 Result")
    
    if exec_result["success"]:
        st.success("✅ Execution successful!")
        
        # Display answer prominently
        st.markdown("### Final Answer:")
        st.markdown(f"## `{exec_result['answer']}`")
        
        # Show answer interpretation if available
        if answer_interpretation:
            st.markdown("---")
            st.markdown("**Interpretation:**")
            st.info(answer_interpretation)
        
        # Show stdout if any
        if exec_result["stdout"].strip():
            with st.expander("📋 Execution Log"):
                st.code(exec_result["stdout"])
    else:
        st.error(f"❌ {exec_result['error_type']}: {exec_result['error']}")
        
        if exec_result["stderr"].strip():
            with st.expander("🐛 Error Details"):
                st.code(exec_result["stderr"])
    
    # Return result for history
    return {
        "problem": problem,
        "source": source,
        "code": code,
        "success": exec_result["success"],
        "answer": exec_result.get("answer"),
        "error": exec_result.get("error")
    }


def main():
    """Main application."""
    st.set_page_config(
        page_title="Math Mentor",
        page_icon="🧮",
        layout="wide"
    )
    
    init_session_state()
    display_header()
    
    # Input mode selector
    st.subheader("📥 Input Mode")
    input_mode = st.radio(
        "Choose input method:",
        ["📝 Text Input", "📷 Image Upload"],
        horizontal=True
    )
    
    problem_text = None
    
    if input_mode == "📝 Text Input":
        # Text input mode (Day 1)
        st.markdown("---")
        st.subheader("Enter Your Math Problem")
        
        problem_text = st.text_area(
            "Problem:",
            placeholder="e.g., Solve x² + 3x - 4 = 0 for x",
            height=100,
            key="problem_input"
        )
        
    else:
        # Image input mode (Day 2)
        st.markdown("---")
        uploaded_file = st.file_uploader(
            "Upload an image of a math problem",
            type=["png", "jpg", "jpeg"],
            help="Take a clear photo of a printed or handwritten math problem"
        )
        
        if uploaded_file:
            problem_text = process_image_input(uploaded_file)
    
    # Show examples
    display_examples()
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        solve_button = st.button("🚀 Solve", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear History", use_container_width=True)
    
    if clear_button:
        st.session_state.history = []
        st.session_state.current_image = None
        st.session_state.extracted_latex = None
        st.rerun()
    
    if solve_button:
        if not problem_text or not problem_text.strip():
            st.warning("⚠️ Please enter a problem first!")
        else:
            st.markdown("---")
            source = "image" if input_mode == "📷 Image Upload" else "text"
            result = solve_problem(problem_text, source)
            
            if result:
                # Add to history
                st.session_state.history.append(result)
    
    # Show history
    if st.session_state.history:
        st.markdown("---")
        st.subheader("📚 Solution History")
        
        for i, item in enumerate(reversed(st.session_state.history), 1):
            source_icon = "📷" if item["source"] == "image" else "📝"
            with st.expander(f"{source_icon} Problem {len(st.session_state.history) - i + 1}: {item['problem'][:60]}..."):
                st.markdown(f"**Problem:** {item['problem']}")
                st.code(item['code'], language="python")
                if item['success']:
                    st.success(f"✅ Answer: `{item['answer']}`")
                else:
                    st.error(f"❌ Error: {item['error']}")


if __name__ == "__main__":
    main()
