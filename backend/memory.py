"""
Conversation Memory Module for Multi-Turn Interactions.
Manages typed conversation history for the Math Mentor.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import time

# Import MathDeck for structured deck storage
try:
    from deck_generator.models import MathDeck
except ImportError:
    MathDeck = None  # Fallback if models not available


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: Literal["user", "assistant", "system"] = Field(
        ..., 
        description="Who sent this message"
    )
    content: str = Field(
        ..., 
        description="The text content of the message (Markdown)"
    )
    deck: Optional[MathDeck] = Field(
        None, 
        description="Optional structured deck for visual explanations"
    )
    timestamp: float = Field(
        default_factory=time.time,
        description="Unix timestamp of when the message was created"
    )
    
    class Config:
        arbitrary_types_allowed = True


import sqlite3
import json
import uuid
from datetime import datetime

DB_PATH = "math_mentor.db"

# Import Episodic Memory
try:
    from episodic_memory import EpisodicMemory
except ImportError:
    EpisodicMemory = None


class ConversationMemory(BaseModel):
    """
    Manages the conversation history for a session with SQLite persistence.
    """
    messages: List[ChatMessage] = Field(default_factory=list)
    active_problem: Optional[str] = Field(None)
    active_answer: Optional[str] = Field(None)
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Private field for episodic memory engine (not serialized by Pydantic)
    _episodic: Optional[object] = None
    
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
    
    def __init__(self, **data):
        super().__init__(**data)
        self._init_db()
        
        # Initialize Episodic Memory (FAISS)
        if EpisodicMemory:
            try:
                self._episodic = EpisodicMemory()
            except Exception as e:
                print(f"Episodic memory disabled: {e}")
                self._episodic = None
                
        # self._load_history() # Off by default, use restore_last_session

    def _init_db(self):
        """Initialize SQLite database."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    deck_json TEXT,
                    timestamp REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    session_id TEXT PRIMARY KEY,
                    active_problem TEXT,
                    active_answer TEXT,
                    last_updated REAL
                )
            """)

    def _load_history(self):
        """Load history from the database for the current session (or most recent)."""
        # Logic moved to explicit restore method to avoid implicit global state
        pass

    def restore_last_session(self) -> bool:
        """
        Attempt to load the most recent conversation from DB.
        Returns: True if restored, False if no history found.
        """
        try:
            with sqlite3.connect(DB_PATH) as conn:
                # Find latest session_id
                cursor = conn.execute("SELECT session_id, active_problem, active_answer FROM conversations ORDER BY last_updated DESC LIMIT 1")
                row = cursor.fetchone()
                
                if row:
                    self.session_id, self.active_problem, self.active_answer = row
                    
                    # Load messages
                    cursor = conn.execute("SELECT role, content, deck_json, timestamp FROM messages WHERE session_id = ? ORDER BY id ASC", (self.session_id,))
                    
                    self.messages = []
                    for role, content, deck_json, ts in cursor.fetchall():
                        deck = None
                        if deck_json and MathDeck:
                            try:
                                deck = MathDeck.model_validate_json(deck_json)
                            except Exception:
                                pass # Ignore deck errors
                        
                        self.messages.append(ChatMessage(
                            role=role, 
                            content=content, 
                            deck=deck, 
                            timestamp=ts
                        ))
                    return True
        except Exception as e:
            print(f"Failed to restore session: {e}")
        return False

    def add_user_message(self, content: str) -> None:
        """Add a user message to the history and DB."""
        msg = ChatMessage(role="user", content=content)
        self.messages.append(msg)
        self._persist_message(msg)
        if self._episodic:
            try:
                self._episodic.add_interaction("user", content, self.session_id)
            except Exception as e:
                print(f"Episodic add failed: {e}")
    
    def add_assistant_message(self, content: str, deck: Optional[MathDeck] = None) -> None:
        """Add an assistant message (with optional deck) and persist."""
        msg = ChatMessage(role="assistant", content=content, deck=deck)
        self.messages.append(msg)
        self._persist_message(msg)
        if self._episodic:
             try:
                self._episodic.add_interaction("assistant", content, self.session_id)
             except Exception: pass

    def _persist_message(self, msg: ChatMessage):
        """Save message to SQLite."""
        deck_json = msg.deck.model_dump_json() if msg.deck else None
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content, deck_json, timestamp) VALUES (?, ?, ?, ?, ?)",
                (self.session_id, msg.role, msg.content, deck_json, msg.timestamp)
            )

    def set_active_problem(self, problem: str, answer: Optional[str] = None) -> None:
        """Set the current problem context and update DB."""
        self.active_problem = problem
        self.active_answer = answer
        # Update conversation state
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO conversations (session_id, active_problem, active_answer, last_updated) VALUES (?, ?, ?, ?)",
                (self.session_id, problem, answer, time.time())
            )

    def clear(self) -> None:
        """Start a fresh session."""
        self.messages = []
        self.active_problem = None
        self.active_answer = None
        self.session_id = str(uuid.uuid4()) # New Session ID

    
    def get_context_window(self, limit: int = 5) -> str:
        """
        Generate a context string for the LLM prompt.
        Returns the last `limit` messages formatted for injection.
        """
        if not self.messages:
            return ""
        
        # Take last N messages
        recent = self.messages[-limit:]
        
        context_parts = []
        
        # Add active problem context if available
        if self.active_problem:
            context_parts.append(f"[ACTIVE PROBLEM]: {self.active_problem}")
            if self.active_answer:
                context_parts.append(f"[COMPUTED ANSWER]: {self.active_answer}")
        
        # Add conversation history
        context_parts.append("\n[CONVERSATION HISTORY]:")
        for msg in recent:
            role_label = "User" if msg.role == "user" else "Math Mentor"
            # Truncate long messages for context
            content = msg.content[:500] + "..." if len(msg.content) > 500 else msg.content
            context_parts.append(f"{role_label}: {content}")
        
        return "\n".join(context_parts)
    
    def is_follow_up(self, new_input: str) -> bool:
        """
        Heuristic to determine if new_input is a follow-up question.
        Returns True if it seems like a follow-up, False if it's a new problem.
        """
        # If no active problem, it's definitely a new problem
        if not self.active_problem:
            return False
        
        # Keywords that suggest a new problem
        new_problem_keywords = [
            "solve", "find", "calculate", "evaluate", "integrate", 
            "differentiate", "factor", "simplify", "expand"
        ]
        
        # Keywords that suggest a follow-up
        follow_up_keywords = [
            "why", "how", "explain", "what", "can you", "tell me more",
            "i don't understand", "step", "again", "that"
        ]
        
        lower_input = new_input.lower().strip()
        
        # Check for explicit math notation (likely a new problem)
        if any(char in new_input for char in ["=", "^", "√", "∫"]):
            return False
        
        # Check for follow-up keywords
        if any(kw in lower_input for kw in follow_up_keywords):
            return True
        
        # Check for new problem keywords
        if any(lower_input.startswith(kw) for kw in new_problem_keywords):
            return False
        
        # Default: if short and no math symbols, likely a follow-up
    def search_memories(self, query: str, top_k: int = 3) -> str:
        """
        Retrieve relevant past interactions from episodic memory.
        Returns formatted string of past conversations.
        """
        if not self._episodic:
            return ""
        try:
            results = self._episodic.recall(query, top_k)
            out = []
            for r in results:
                 # Filter out current session if needed? For now include all.
                 role = r.get('role', 'unknown').upper()
                 content = r.get('content', '').strip()
                 out.append(f"PAST INTERACTION ({role}): {content}")
            return "\n\n".join(out)
        except Exception:
            return ""
