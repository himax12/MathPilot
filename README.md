# 🧮 Math Mentor AI

Math Mentor is an advanced, Study-Buddy AI that uses a **Multi-Agent Reflexion Architecture** to solve math problems, verify solutions, and generate interactive visual explanations.

It goes beyond simple LLM generation by implementing a rigorous pipeline:
**Parse** → **Route** → **Solve (Program-of-Thoughts)** → **Verify (SymPy)** → **Reflect (Self-Correction)**.

---

## 🏗️ Architecture

The system is orchestrated by a central generic agent that coordinates specialized sub-agents.

```mermaid
graph TD
    User([User]) <-->|Chat/Image/Audio| Frontend[Streamlit App]
    
    subgraph "Backend System"
        Frontend <--> Orchestrator
        
        Orchestrator --> Parser[Parser Agent]
        Orchestrator --> Router[Router Agent]
        
        subgraph "Reflexion Loop"
            Orchestrator <--> Solver[Solver Agent]
            Solver <--> Verifier[Verifier Agent]
        end
        
        Solver <-->|Retrieval| RAG[MathRAG (Knowledge Base)]
        Solver <-->|History| Memory[SQLite + FAISS Memory]
        
        Solver -->|Code| Python[Python Sandbox (SymPy)]
        Verifier -->|Code| Python
    end
```

## ✨ Key Features

- **🧠 Multi-Agent Orchestrator**: Uses a `Reflexion` workflow (Solve -> Verify -> Reflect) to self-correct errors before showing the answer.
- **📚 RAG Knowledge Base**: Retrieves verified math concepts from a curated textbook library (`backend/knowledge`) to ground the solution.
- **🛡️ Verifier Agent**: Executes generated SymPy code in a sandbox to mathematically guarantee correctness.
- **📊 Interactive Visuals**: Generates `MathDeck` visualizations (graphs, diagrams) for geometric and algebraic concepts.
- **💾 Long-Term Memory**:
  - **Episodic**: Remembers past conversations using semantic search (FAISS).
  - **Persistent**: Stores chat history in SQLite (`math_mentor.db`).
- **👁️ Multimodal Input**: Supports text, handwriting (OCR), and voice (Google Chirp).

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- `uv` package manager (recommended)
- Google Gemini API Key
- Google Cloud Project (for Speech-to-Text)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/math-mentor.git
   cd math-mentor
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure Environment**:
   Create a `.env` file based on `.env.example`:
   ```bash
   GEMINI_API_KEY=your_api_key
   GCP_PROJECT_ID=your_project_id
   ```

### Running the App

Start the Streamlit interface:
```bash
uv run streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## 🧪 Testing

Run the comprehensive test suite:
```bash
uv run pytest tests/
```

Or run specific agent tests:
```bash
uv run python tests/test_orchestrator.py
uv run python tests/test_verifier.py
```

## 📂 Project Structure

- `backend/agents/`: specialized agents (Solver, Verifier, Router, Parser).
- `backend/knowledge/`: RAG system and textbook markdown files.
- `backend/orchestrator.py`: Main state machine logic.
- `frontend/`: Streamlit UI components.
- `tests/`: Unit and end-to-end tests.

---
*Built with ❤️ by Antigravity*
