from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import dataclasses
import json
import base64
import logging
import sys
import traceback

# ─── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mathpilot.api")
logger.info("=" * 60)
logger.info("MathPilot API starting up...")
logger.info("=" * 60)

# ─── Backend Imports ──────────────────────────────────────────────────────────
try:
    logger.info("Importing Orchestrator and DeckGenerator...")
    from backend.orchestrator import Orchestrator
    from backend.deck_generator import DeckGenerator
    logger.info("✅ Orchestrator and DeckGenerator imported OK")
except Exception as e:
    logger.critical(f"❌ FATAL: Could not import Orchestrator: {e}")
    logger.critical(traceback.format_exc())
    raise

try:
    logger.info("Importing OCR process_image...")
    from backend.ocr import process_image
    logger.info("✅ OCR imported OK")
except Exception as e:
    logger.warning(f"⚠️  OCR import failed (non-fatal): {e}")
    def process_image(b64): return {"latex": "", "problem_data": {}}

# ─── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(title="MathPilot API")

# Enable CORS for React frontend (Vite defaults to 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global Orchestrator ───────────────────────────────────────────────────────
try:
    logger.info("Initializing Orchestrator (this loads all 5 agents)...")
    orchestrator = Orchestrator()
    logger.info("✅ Orchestrator initialized")
    
    logger.info("Initializing DeckGenerator...")
    deck_generator = DeckGenerator(theme="dark")
    logger.info("✅ DeckGenerator initialized")
    
    logger.info("Restoring last session...")
    orchestrator.restore_session()
    logger.info("✅ Session restored")
except Exception as e:
    logger.critical(f"❌ FATAL: Orchestrator initialization failed: {e}")
    logger.critical(traceback.format_exc())
    raise

logger.info("=" * 60)
logger.info("🚀 MathPilot API ready — all agents loaded successfully")
logger.info("=" * 60)

# ─── Request Models ────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str | dict  # str for text, dict for OCR {"latex": "...", "problem_data": {...}}

class FeedbackRequest(BaseModel):
    problem: str
    wrong_answer: str
    correct_answer: str
    explanation: str

# ─── Helpers ──────────────────────────────────────────────────────────────────
def _serialize_dict(obj):
    """Helper to heavily serialize dataclasses or pydantic objects safely to dict"""
    if obj is None:
         return None
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return obj

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/api/chat")
def chat(request: ChatRequest):
    logger.info(f"POST /api/chat — message type: {type(request.message).__name__}, preview: {str(request.message)[:80]}")
    
    def generate():
        try:
            for chunk in orchestrator.run_stream(request.message):
                if chunk["type"] == "final":
                    result = chunk["data"]
                    logger.info(f"Orchestrator returned status={result.get('status', 'N/A')}, confidence={result.get('confidence', 'N/A')}")

                    ctx = result.get("context")
                    explanation = ctx.explanation if ctx and hasattr(ctx, "explanation") else None
                    
                    deck_obj = result.get("deck")
                    deck_html = None
                    if deck_obj:
                        try:
                            deck_html = deck_generator.from_structured(deck_obj)
                        except Exception as e:
                            logger.error(f"Failed to generate deck_html: {e}")

                    out = {
                        "response": result.get("response"),
                        "events": result.get("events"),
                        "confidence": result.get("confidence"),
                        "status": result.get("status", "success"),
                        "deck": _serialize_dict(deck_obj),
                        "deck_html": deck_html,
                        "explanation": _serialize_dict(explanation)
                    }
                    chunk["data"] = out
                    logger.debug(f"Returning final chat response — events count: {len(out['events'] or [])}")
                
                yield json.dumps(chunk) + "\n"

        except Exception as e:
            logger.error(f"❌ /api/chat stream failed: {e}")
            logger.error(traceback.format_exc())
            yield json.dumps({"type": "error", "data": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")

@app.get("/api/sessions")
def get_sessions():
    logger.debug("GET /api/sessions")
    try:
        sessions = orchestrator.solver.memory.get_all_sessions()
        logger.debug(f"Returning {len(sessions)} sessions")
        return {"sessions": sessions}
    except Exception as e:
        logger.error(f"❌ /api/sessions failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/{session_id}/restore")
def restore_session(session_id: str):
    logger.info(f"POST /api/sessions/{session_id}/restore")
    try:
        success = orchestrator.solver.memory.restore_session_by_id(session_id)
        if success:
            messages = []
            for msg in orchestrator.solver.memory.messages:
                deck_html = None
                if msg.deck:
                    try:
                        deck_html = deck_generator.from_structured(msg.deck)
                    except Exception as e:
                        logger.error(f"Failed to generate deck_html for restore: {e}")
                        
                msg_data = {
                    "role": msg.role,
                    "content": msg.content,
                    "events": getattr(msg, 'events', []),
                    "deck": _serialize_dict(msg.deck),
                    "deck_html": deck_html,
                    "explanation": _serialize_dict(getattr(msg, 'explanation', None)),
                    "confidence": getattr(msg.solution_state, 'confidence', None) if getattr(msg, 'solution_state', None) else None,
                    "rag_context": getattr(msg.solution_state, 'rag_context', None) if getattr(msg, 'solution_state', None) else None,
                }
                messages.append(msg_data)
            logger.info(f"Restored session {session_id}: {len(messages)} messages")
            return {"success": True, "messages": messages}
        logger.warning(f"Session {session_id} not found")
        return {"success": False}
    except Exception as e:
        logger.error(f"❌ /api/sessions/restore failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/clear")
def clear_session():
    logger.info("POST /api/sessions/clear")
    try:
        orchestrator.clear_conversation()
        return {"success": True}
    except Exception as e:
        logger.error(f"❌ /api/sessions/clear failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):
    logger.info(f"POST /api/feedback — problem: {request.problem[:60]}")
    try:
        orchestrator.solver.memory.add_feedback(
            problem=request.problem,
            wrong_answer=request.wrong_answer,
            correct_answer=request.correct_answer,
            explanation=request.explanation
        )
        return {"success": True}
    except Exception as e:
        logger.error(f"❌ /api/feedback failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), type: str = Form("image")):
    logger.info(f"POST /api/upload — filename: {file.filename}, type: {type}")
    if type == "image":
        try:
            contents = await file.read()
            logger.debug(f"Read {len(contents)} bytes from uploaded file")
            b64_img = base64.b64encode(contents).decode("utf-8")
            ocr_result = process_image(b64_img)
            logger.info(f"OCR result: latex length={len(ocr_result.get('latex', ''))}")
            return {
                "success": True,
                "latex": ocr_result.get("latex", ""),
                "problem_data": ocr_result.get("problem_data", {})
            }
        except Exception as e:
            logger.error(f"❌ /api/upload failed: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    return {"success": False, "error": "Unsupported type"}
