# Math Mentor - Vertical Slice MVP

An AI-powered math problem solver that uses **Program-of-Thoughts (PoT)** pattern to generate and execute SymPy code for reliable mathematical solutions.

## 🚀 Quick Start

### 1. Setup

```bash
# Clone/navigate to project
cd math-mentor

# Install dependencies (using uv)
uv sync

# Configure API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Run

```bash
# Start Streamlit app
uv run streamlit run frontend/app.py
```

### 3. Use

1. Enter a math problem (algebra, calculus, probability)
2. Click "Solve"
3. See generated SymPy code + answer

## 🏗️ Architecture

### Complete Flow: Image/Text → Answer

```
Input (Text OR Image)
    ↓
[If Image] OCR (Cloud Vision + Gemini Vision)
    ↓
Bidirectional Verification (Side-by-side LaTeX render)
    ↓
HITL (Edit if confidence < 70% OR user wants to correct)
    ↓
Solver Agent (Gemini → SymPy Code)
    ↓
Executor (Sandboxed Python)
    ↓
Answer Display
```

**Key Components:**
- `backend/solver.py`: Generates SymPy code using Gemini API
- `backend/executor.py`: Executes code safely with timeout
- `backend/ocr.py`: Dual-model OCR (Cloud Vision + Gemini Vision)
- `frontend/app.py`: Streamlit UI with image upload + text input

### Day 1 (Complete): Text → Answer ✅

- Text input for math problems
- SymPy code generation via Gemini
- Sandboxed code execution
- Answer display with code trace

### Day 2 (Complete): Image OCR + HITL ✅

- Image upload with Google Cloud Vision API
- Gemini Vision fallback for semantic extraction
- **Bidirectional verification** (side-by-side LaTeX render)
- **Confidence-based HITL** (< 70% triggers manual review)
- Editable LaTeX before solving

## 🧪 Testing

```bash
# Test solver and executor
uv run python tests/test_solver.py

# Run app locally
uv run streamlit run frontend/app.py
```

## 📝 Example Problems

**Algebra:**
- Solve x² + 3x - 4 = 0 for x
- Factor x² - 9

**Calculus:**
- Integrate x² from 0 to 10
- Find derivative of sin(x) * cos(x)

**Probability:**
- P(X < 2) where X ~ Normal(0, 1)

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full guide.

**Quick Deploy to Streamlit Cloud:**
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `GEMINI_API_KEY` to secrets
5. Deploy!

## 🛠️ Tech Stack

- **LLM**: Google Gemini 2.0 Flash (Exp)
- **OCR**: Google Cloud Vision + Gemini Vision
- **Math Engine**: SymPy
- **Frontend**: Streamlit
- **Package Manager**: uv

## 📂 Project Structure

```
math-mentor/
├── backend/
│   ├── solver.py       # Code generation agent
│   ├── executor.py     # Safe code execution
│   └── ocr.py          # Image → LaTeX extraction
├── frontend/
│   └── app.py          # Streamlit UI (text + image)
├── tests/
│   └── test_solver.py  # Test suite
├── .env.example
├── requirements.txt
├── DEPLOYMENT.md
└── README.md
```

## 🎯 MVP Scope (2 Days - Complete!)

**Day 1 (Complete) ✅:**
- ✅ Text input
- ✅ SymPy code generation
- ✅ Sandboxed execution
- ✅ Basic Streamlit UI

**Day 2 (Complete) ✅:**
- ✅ Image OCR (dual-model)
- ✅ Bidirectional LaTeX verification
- ✅ HITL (confidence-based)
- ✅ Deployment-ready

**Deferred to Post-MVP:**
- ⏳ RAG pipeline (knowledge base)
- ⏳ Memory/caching (template reuse)
- ⏳ Multi-agent orchestration (LangGraph)
- ⏳ Audio input (Whisper)
- ⏳ Advanced verifier (symbolic cross-check)

## 🎬 Demo

1. **Text Mode**: Enter "Solve x² + 3x - 4 = 0" → See code + answer
2. **Image Mode**: Upload photo → Verify LaTeX → Solve

## 📄 License

MIT
