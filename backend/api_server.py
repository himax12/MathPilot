"""
FastAPI Server for Math Mentor
Connects Next.js frontend with Python backend agents.
"""

import sys
import os
import asyncio
import json
import base64
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Add backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import backend components
try:
    from orchestrator import Orchestrator
    from ocr import MathOCR
    from input.asr import MathASR
    from config import config
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure to run from the backend directory")
    raise

# Global instances (initialized at startup)
orchestrator: Optional[Orchestrator] = None
ocr: Optional[MathOCR] = None
asr: Optional[MathASR] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize components at startup."""
    global orchestrator, ocr, asr
    
    print("🚀 Starting Math Mentor API Server...")
    
    # Initialize orchestrator
    try:
        orchestrator = Orchestrator()
        print("✅ Orchestrator initialized")
    except Exception as e:
        print(f"⚠️ Orchestrator init failed: {e}")
        orchestrator = None
    
    # Initialize OCR
    try:
        ocr = MathOCR()
        print("✅ OCR initialized")
    except Exception as e:
        print(f"⚠️ OCR init failed: {e}")
        ocr = None
    
    # Initialize ASR
    try:
        asr = MathASR()
        print("✅ ASR initialized" if asr.client else "⚠️ ASR not configured")
    except Exception as e:
        print(f"⚠️ ASR init failed: {e}")
        asr = None
    
    yield
    
    print("👋 Shutting down Math Mentor API Server")


# Create FastAPI app
app = FastAPI(
    title="Math Mentor API",
    description="API for AI-powered math tutoring",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Request/Response Models =====

class SolveRequest(BaseModel):
    problem: str
    mode: str = "solve"  # solve, explain, practice, graph
    image: Optional[str] = None  # Base64 encoded image

class SolveResponse(BaseModel):
    success: bool
    solution: str
    steps: Optional[list] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None

class OCRResponse(BaseModel):
    success: bool
    text: str
    problem_data: Optional[dict] = None
    confidence: float = 0.0
    error: Optional[str] = None

class TranscribeResponse(BaseModel):
    success: bool
    text: str
    confidence: float = 0.0
    error: Optional[str] = None


# ===== Endpoints =====

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "orchestrator": orchestrator is not None,
        "ocr": ocr is not None,
        "asr": asr is not None and asr.client is not None,
    }


@app.post("/api/solve", response_model=SolveResponse)
async def solve_problem(request: SolveRequest):
    """
    Solve a math problem using the Orchestrator.
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        # If image provided, run OCR first
        problem_text = request.problem
        ocr_extracted = None
        
        if request.image and ocr:
            print("📷 Processing image with OCR...")
            image_bytes = base64.b64decode(request.image)
            ocr_result = ocr.extract_from_image(image_bytes)
            
            # Extract the full problem text from OCR result
            problem_data = ocr_result.get("problem_data", {})
            if isinstance(problem_data, dict):
                ocr_extracted = problem_data.get("problem_text_full", "")
            elif ocr_result.get("latex"):
                ocr_extracted = ocr_result["latex"]
            
            if ocr_extracted:
                print(f"📝 OCR extracted: {ocr_extracted[:100]}...")
                # Use OCR text as primary problem, with user text as context
                if request.problem.strip():
                    problem_text = f"{request.problem}\n\nProblem from image:\n{ocr_extracted}"
                else:
                    problem_text = ocr_extracted
        
        print(f"🧮 Solving: {problem_text[:100]}...")
        
        # Run orchestrator
        result = orchestrator.run(problem_text)
        
        # Format response
        solution_text = result.get("response", "")
        
        return SolveResponse(
            success=True,
            solution=solution_text,
            metadata={
                "events": result.get("events", []),
                "status": result.get("status", ""),
                "ocr_extracted": ocr_extracted,
            }
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return SolveResponse(
            success=False,
            solution="",
            error=str(e)
        )


@app.post("/api/solve/stream")
async def solve_problem_stream(request: SolveRequest):
    """
    Stream a solution using Server-Sent Events.
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    async def generate() -> AsyncGenerator[str, None]:
        try:
            # If image provided, run OCR first
            problem_text = request.problem
            
            if request.image and ocr:
                print("📷 [Stream] Processing image with OCR...")
                image_bytes = base64.b64decode(request.image)
                ocr_result = ocr.extract_from_image(image_bytes)
                
                # Extract the full problem text from OCR result
                problem_data = ocr_result.get("problem_data", {})
                ocr_extracted = None
                if isinstance(problem_data, dict):
                    ocr_extracted = problem_data.get("problem_text_full", "")
                elif ocr_result.get("latex"):
                    ocr_extracted = ocr_result["latex"]
                
                if ocr_extracted:
                    print(f"📝 [Stream] OCR extracted: {ocr_extracted[:100]}...")
                    if request.problem.strip():
                        problem_text = f"{request.problem}\n\nProblem from image:\n{ocr_extracted}"
                    else:
                        problem_text = ocr_extracted
            
            print(f"🧮 [Stream] Solving: {problem_text[:100]}...")
            
            # Run orchestrator (this is blocking, so we run in thread)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, orchestrator.run, problem_text)
            
            # Stream the solution character by character
            solution = result.get("response", "")
            
            # Stream in chunks for realistic effect
            chunk_size = 5
            for i in range(0, len(solution), chunk_size):
                chunk = solution[i:i + chunk_size]
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0.02)  # Small delay for streaming effect
            
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/ocr", response_model=OCRResponse)
async def extract_from_image(image: UploadFile = File(...)):
    """
    Extract math expression from an uploaded image.
    """
    if not ocr:
        raise HTTPException(status_code=503, detail="OCR not initialized")
    
    try:
        image_bytes = await image.read()
        result = ocr.extract_from_image(image_bytes)
        
        return OCRResponse(
            success=result.get("error") is None,
            text=result.get("latex", ""),
            problem_data=result.get("problem_data"),
            confidence=result.get("confidence", 0.0),
            error=result.get("error")
        )
        
    except Exception as e:
        return OCRResponse(
            success=False,
            text="",
            error=str(e)
        )


@app.post("/api/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio to text.
    """
    if not asr or not asr.client:
        raise HTTPException(status_code=503, detail="ASR not configured")
    
    try:
        audio_bytes = await audio.read()
        result = asr.transcribe(audio_bytes)
        
        return TranscribeResponse(
            success=result.get("error") is None,
            text=result.get("text", ""),
            confidence=result.get("confidence", 0.0),
            error=result.get("error")
        )
        
    except Exception as e:
        return TranscribeResponse(
            success=False,
            text="",
            error=str(e)
        )


@app.get("/api/history")
async def get_history():
    """
    Get chat history (placeholder for future implementation).
    """
    # TODO: Implement with episodic memory
    return []


# ===== Run Server =====

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"Starting server at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=True)
