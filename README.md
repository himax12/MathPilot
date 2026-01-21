# Math Mentor: logical-reasoning-agent
A deterministic, multi-agent system for robust mathematical problem solving.

## Project Overview

Math Mentor is an autonomous reasoning system designed to solve high-school and undergraduate level mathematics problems with high reliability. Unlike varied "chat" interfaces, this application decouples reasoning (Large Language Models) from computation (Symbolic Python), using a multi-agent architecture to ensure accuracy, verifiability, and self-correction.

The system accepts multimodal inputs (text, image, audio) and employs a Human-in-the-Loop (HITL) workflow to handle ambiguity before it propagates to the solver.

## Core Philosophy

1.  **Separation of Concerns**: LLMs are excellent at planning and translation but poor at arithmetic. This system uses Gemini 2.0 Flash solely for semantic understanding and code generation, while offloading all logic to a Python sandbox (SymPy).
2.  **Reflexion**: A unified Orchestrator manages a feedback loop where failures in solution verification trigger immediate introspection and strategy adjustment, rather than silent failure.
3.  **Episodic Memory**: The system persists successful solution patterns. When faced with a new problem, it retrieves semantically similar past successes to guide its current strategy (Self-Learning).

## System Architecture

The application is structured as a pipeline of specialized agents coordinated by a central Orchestrator.

### 1. Input Processing Layer
*   **OCR Engine**: Uses Google Gemini Vision (Program-of-Thought prompting) to transcribe mathematical images into structured text. Includes transparency handling and contrast optimization.
*   **ASR Engine**: Uses Gemini Audio models to transcribe spoken mathematical queries, converting natural speech into formal problem statements.

### 2. Cognitive Layer (The Agents)
*   **Parser Agent**: Normalizes raw input into a structured schema, identifying variables, constraints, and specifically "what needs to be solved". Flags ambiguous input for user clarification.
*   **Router Agent**: Classifies intent (e.g., Algebra, Probability, Calculus) to select the optimal solving strategy and filter the knowledge base.
*   **Solver Agent**: The core reasoning engine. It adopts a "Program-of-Thought" approach, generating SymPy code to solve problems deterministically. It integrates RAG to access mathematical laws and theorems.
*   **Verifier Agent**: A "Judge" model that validates solutions by:
    1.  Numerical Substitution (plugging answers back into equations).
    2.  Conceptual Sanity Checks (validating units, domains, and bounds).
*   **Explainer (DeckGen + Solver)**: Rather than a redundant text summarizer, the system uses a specialized **Visual Deck Generator**. This component takes the Solver's logical trace and transforms it into a step-by-step visual presentation (HTML/CSS), acting as the "Tutor" that explains the *why* and *how* alongside the *what*.

### 3. Memory & Persistence
*   **Vector Store (FAISS)**: Stores embeddings of past interactions.
*   **Relational DB (SQLite)**: Logs full conversation history, user feedback, and verification states.

### System Diagram

```mermaid
flowchart TD
    %% Nodes
    User([User])
    UI[Frontend Interface]
    Orchestrator{Orchestrator}
    DeckGen[Visual Explainer<br>(Deck Generator)]
    
    subgraph Perception ["Perception Layer"]
        OCR[OCR Engine]
        ASR[ASR Engine]
    end
    
    subgraph Agents ["Cognitive Layer"]
        Parser[Parser Agent]
        Solver[Solver Agent]
        Verifier[Verifier Agent]
    end
    
    subgraph Memory ["Memory System"]
        RAG[(Knowledge Base)]
        History[(Episodic Memory)]
    end
    
    %% Edges
    User <--> UI
    UI -->|Image| OCR
    UI -->|Audio| ASR
    UI -->|Text| Orchestrator
    OCR --> Orchestrator
    ASR --> Orchestrator
    
    %% Core Loop
    Orchestrator --> Parser
    Parser -->|Structured JSON| Orchestrator
    
    Orchestrator -->|Problem + Context| Solver
    Solver <-->|Retrieve Similar| History
    Solver <-->|Retrieve Knowledge| RAG
    
    Solver -->|Python Code| Verifier
    Verifier -->|Substitution Check| Orchestrator
    
    Orchestrator -.->|Reflexion Retry| Solver
    
    Orchestrator -->|Verified Trace| DeckGen
    DeckGen -->|Visual Deck| UI
```

## Technology Stack

*   **Frontend**: Streamlit (Python)
*   **LLM Orchestration**: Google Gemini 2.0 Flash & Pro
*   **Symbolic Math**: SymPy, NumPy
*   **Vector Search**: FAISS
*   **Backend Framework**: Python 3.10+

## Setup & Installation

### Prerequisites
*   Python 3.10 or higher
*   Google Cloud API Key (for Gemini)

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd math-mentor
    ```

2.  **Install dependencies**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

4.  **Run the Application**
    ```bash
    streamlit run frontend/app.py
    ```

## Usage Guide

1.  **Select Input Mode**: Use the sidebar to switch between Text, Image Upload, or Audio Recording.
2.  **Submit Problem**: Enter the math problem. The system will first parse and validate the input.
3.  **Review Plan**: The "Thinking Process" expander visualizes the real-time agent workflow (Parsing -> Retrieval -> Planning -> Verification).
4.  **Verify & Explain**: The final output includes the computed answer, a step-by-step derivation, and (where applicable) dynamic visual aids.
5.  **Feedback**: Use the Thumbs Up/Down and "Edit" buttons to provide feedback, which is stored to improve future performance.
