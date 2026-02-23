from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import dataclasses
import json
import base64
import logging
import sys
import traceback
import os
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

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

try:
    logger.info("Importing ASR MathASR...")
    from backend.input.asr import MathASR
    asr_handler = MathASR()
    logger.info("✅ ASR imported and initialized OK")
except Exception as e:
    logger.warning(f"⚠️  ASR init failed (non-fatal): {e}")
    asr_handler = None

try:
    logger.info("Importing Rate Limiter...")
    from backend.rate_limiter import rate_limiter, SubscriptionTier
    logger.info("✅ Rate Limiter imported OK")
except Exception as e:
    logger.critical(f"❌ FATAL: Could not import Rate Limiter: {e}")
    logger.critical(traceback.format_exc())
    raise

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

class AuthGoogleRequest(BaseModel):
    credential: str

class FeedbackRequest(BaseModel):
    problem: str
    wrong_answer: str
    correct_answer: str
    explanation: str

class TitleUpdateRequest(BaseModel):
    title: str

# ─── Helpers ──────────────────────────────────────────────────────────────────
# ─── Auth Helpers ──────────────────────────────────────────────────────────────
security = HTTPBearer()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET", "math-pilot-super-secret-key-123")
ALGORITHM = "HS256"

def verify_google_token(token: str):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError:
        # Invalid token
        return None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

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

@app.post("/api/auth/google")
def auth_google(request: AuthGoogleRequest):
    logger.info(f"=== Google Auth Request Received ===")
    logger.info(f"Credential length: {len(request.credential) if request.credential else 0}")
    
    if not GOOGLE_CLIENT_ID or GOOGLE_CLIENT_ID == "your_google_oauth_client_id_here":
        logger.error("⚠️  GOOGLE_CLIENT_ID not configured in environment variables")
        logger.error(f"Current value: {GOOGLE_CLIENT_ID}")
        raise HTTPException(
            status_code=500, 
            detail="Server configuration error: GOOGLE_CLIENT_ID not set. Please configure OAuth credentials."
        )
    
    logger.debug(f"Verifying Google token (Client ID: {GOOGLE_CLIENT_ID[:20]}...)")
    idinfo = verify_google_token(request.credential)
    
    if not idinfo:
        logger.error("❌ Invalid Google token received")
        logger.error(f"Token verification failed for Client ID: {GOOGLE_CLIENT_ID[:20]}...")
        raise HTTPException(status_code=400, detail="Invalid Google token. Token verification failed.")
    
    user_id = idinfo['sub']
    email = idinfo.get('email')
    name = idinfo.get('name')
    picture = idinfo.get('picture')
    
    logger.info(f"✅ User authenticated: {email} ({user_id})")
    
    # Save user info to DB
    orchestrator.solver.memory.add_user_info(user_id, email, name, picture)
    
    # Create internal JWT
    token = create_access_token({"sub": user_id, "email": email, "name": name})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": email,
            "name": name,
            "picture": picture
        }
    }

@app.post("/api/chat")
def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    
    # Rate limit check
    allowed, limit_info = rate_limiter.check_rate_limit(user_id)
    if not allowed:
        logger.warning(f"Rate limit exceeded for user {user_id}: {limit_info['used_today']}/{limit_info['daily_limit']}")
        raise HTTPException(
            status_code=429, 
            detail={
                "error": "Rate limit exceeded",
                "message": f"You've used {limit_info['used_today']} of {limit_info['daily_limit']} daily prompts.",
                "limit_info": limit_info
            }
        )
    
    # Log usage
    rate_limiter.log_usage(user_id, endpoint="/api/chat")
    
    orchestrator.solver.memory.user_id = user_id
    logger.info(f"POST /api/chat — user: {user_id}, usage: {limit_info['used_today']}/{limit_info['daily_limit']}, message type: {type(request.message).__name__}, preview: {str(request.message)[:80]}")
    
    def generate():
        try:
            for chunk in orchestrator.run_stream(request.message, user_id=user_id):
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
def get_sessions(user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    logger.debug(f"GET /api/sessions — user: {user_id}")
    try:
        sessions = orchestrator.solver.memory.get_all_sessions(user_id)
        logger.debug(f"Returning {len(sessions)} sessions")
        return {"sessions": sessions}
    except Exception as e:
        logger.error(f"❌ /api/sessions failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/sessions/{session_id}")
def update_session(session_id: str, request: TitleUpdateRequest, user: dict = Depends(get_current_user)):
    logger.info(f"PUT /api/sessions/{session_id} — user: {user['sub']}, title: {request.title}")
    try:
        orchestrator.solver.memory.update_title(request.title, session_id)
        return {"success": True}
    except Exception as e:
        logger.error(f"❌ /api/sessions/{session_id} update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str, user: dict = Depends(get_current_user)):
    logger.info(f"DELETE /api/sessions/{session_id} — user: {user['sub']}")
    try:
        success = orchestrator.solver.memory.delete_session(session_id)
        return {"success": success}
    except Exception as e:
        logger.error(f"❌ /api/sessions/{session_id} deletion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sessions/{session_id}/restore")
def restore_session(session_id: str, user: dict = Depends(get_current_user)):
    logger.info(f"POST /api/sessions/{session_id}/restore — user: {user['sub']}")
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
def clear_session(user: dict = Depends(get_current_user)):
    logger.info(f"POST /api/sessions/clear — user: {user['sub']}")
    try:
        orchestrator.clear_conversation()
        return {"success": True}
    except Exception as e:
        logger.error(f"❌ /api/sessions/clear failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest, user: dict = Depends(get_current_user)):
    logger.info(f"POST /api/feedback — user: {user['sub']}, problem: {request.problem[:60]}")
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
async def upload_file(file: UploadFile = File(...), type: str = Form("image"), user: dict = Depends(get_current_user)):
    logger.info(f"POST /api/upload — user: {user['sub']}, filename: {file.filename}, type: {type}")
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


@app.post("/api/asr")
async def transcribe_audio(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    logger.info(f"POST /api/asr — user: {user['sub']}, filename: {file.filename}")
    if not asr_handler:
        raise HTTPException(status_code=501, detail="ASR service not available (check GCP config)")
        
    try:
        contents = await file.read()
        logger.debug(f"Read {len(contents)} bytes from audio file")
        
        result = asr_handler.transcribe(contents)
        logger.info(f"ASR result: text='{result.get('text', '')}', confidence={result.get('confidence', 0)}")
        
        if result.get("error"):
            return {"success": False, "error": result["error"]}
            
        return {
            "success": True,
            "text": result.get("text", ""),
            "confidence": result.get("confidence", 0)
        }
    except Exception as e:
        logger.error(f"❌ /api/asr failed: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# ─── Billing & Subscription Routes ────────────────────────────────────────────

@app.get("/api/billing/plans")
def get_plans():
    """Get all available subscription plans."""
    return rate_limiter.get_all_plans()


@app.get("/api/billing/usage")
def get_usage(user: dict = Depends(get_current_user)):
    """Get current user's usage and subscription info."""
    user_id = user["sub"]
    logger.debug(f"GET /api/billing/usage — user: {user_id}")
    
    try:
        allowed, limit_info = rate_limiter.check_rate_limit(user_id)
        subscription_info = rate_limiter.get_subscription_info(user_id)
        
        return {
            "allowed": allowed,
            "limit_info": limit_info,
            "subscription": subscription_info
        }
    except Exception as e:
        logger.error(f"❌ /api/billing/usage failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/billing/upgrade")
def upgrade_plan(tier: str, user: dict = Depends(get_current_user)):
    """
    Upgrade to a new subscription tier.
    
    NOTE: This is a simplified endpoint. In production, integrate with Stripe:
    1. Create Stripe checkout session
    2. User completes payment
    3. Stripe webhook confirms payment
    4. Then call rate_limiter.upgrade_subscription()
    """
    user_id = user["sub"]
    logger.info(f"POST /api/billing/upgrade — user: {user_id}, tier: {tier}")
    
    try:
        # Validate tier
        if tier not in [t.value for t in SubscriptionTier]:
            raise HTTPException(status_code=400, detail="Invalid subscription tier")
        
        target_tier = SubscriptionTier(tier)
        
        # For demo purposes, allow direct upgrade (in production, require payment first)
        success = rate_limiter.upgrade_subscription(user_id, target_tier)
        
        if success:
            return {
                "success": True,
                "message": f"Successfully upgraded to {target_tier.value} plan",
                "subscription": rate_limiter.get_subscription_info(user_id)
            }
        else:
            raise HTTPException(status_code=500, detail="Upgrade failed")
            
    except Exception as e:
        logger.error(f"❌ /api/billing/upgrade failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/billing/cancel")
def cancel_subscription(user: dict = Depends(get_current_user)):
    """Cancel subscription and downgrade to free tier."""
    user_id = user["sub"]
    logger.info(f"POST /api/billing/cancel — user: {user_id}")
    
    try:
        success = rate_limiter.cancel_subscription(user_id)
        
        if success:
            return {
                "success": True,
                "message": "Subscription cancelled. Downgraded to Free plan.",
                "subscription": rate_limiter.get_subscription_info(user_id)
            }
        else:
            raise HTTPException(status_code=500, detail="Cancellation failed")
            
    except Exception as e:
        logger.error(f"❌ /api/billing/cancel failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files from the built React app (dist folder)
# We expect the 'dist' contents to be placed in backend/static during build
static_dir = os.path.join(os.path.dirname(__file__), "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Prevent interfering with API routes
        if full_path.startswith("api"):
             raise HTTPException(status_code=404)
             
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    logger.warning(f"⚠️ Static directory not found at {static_dir}. Frontend will not be served.")
