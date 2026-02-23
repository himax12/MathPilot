"""
Rate Limiter Module - Manages API usage limits and subscription tiers.

Implements a clean tiered pricing model:
- FREE: 10 prompts per day
- STANDARD: $5/month - 25 calls per day
- PRO: $20/month - 100 requests per day  
- PREMIUM: $200/month - 1000 requests per day
- CUSTOM: $20 per 100 requests (pay-as-you-go)
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "math_mentor.db")


class SubscriptionTier(str, Enum):
    """Subscription tier definitions."""
    FREE = "free"
    STANDARD = "standard"
    PRO = "pro"
    PREMIUM = "premium"
    CUSTOM = "custom"


@dataclass
class PlanDetails:
    """Details of a subscription plan."""
    tier: SubscriptionTier
    name: str
    price_monthly: float  # USD
    daily_limit: int
    description: str
    features: list


# Plan Definitions
PLANS = {
    SubscriptionTier.FREE: PlanDetails(
        tier=SubscriptionTier.FREE,
        name="Free Plan",
        price_monthly=0.0,
        daily_limit=10,
        description="Perfect for trying out Math Mentor",
        features=["10 problems per day", "Basic solving", "Visual explanations"]
    ),
    SubscriptionTier.STANDARD: PlanDetails(
        tier=SubscriptionTier.STANDARD,
        name="Standard Plan",
        price_monthly=5.0,
        daily_limit=25,
        description="For regular students",
        features=["25 problems per day", "Advanced solving", "Priority support", "RAG knowledge base"]
    ),
    SubscriptionTier.PRO: PlanDetails(
        tier=SubscriptionTier.PRO,
        name="Pro Plan",
        price_monthly=20.0,
        daily_limit=100,
        description="For serious learners and tutors",
        features=["100 problems per day", "All features", "Fast processing", "API access"]
    ),
    SubscriptionTier.PREMIUM: PlanDetails(
        tier=SubscriptionTier.PREMIUM,
        name="Premium Plan",
        price_monthly=200.0,
        daily_limit=1000,
        description="For educational institutions",
        features=["1000 problems per day", "Priority processing", "Custom integrations", "Dedicated support"]
    ),
    SubscriptionTier.CUSTOM: PlanDetails(
        tier=SubscriptionTier.CUSTOM,
        name="Pay-as-you-go",
        price_monthly=0.0,  # Charged per use
        daily_limit=999999,  # Virtually unlimited
        description="$20 per 100 requests",
        features=["No daily limit", "Pay only for what you use", "Flexible billing"]
    )
}


class RateLimiter:
    """
    Manages rate limiting and subscription enforcement.
    
    Design principles:
    - Daily limits reset at midnight UTC
    - Usage is tracked per user per day
    - Clean separation between free and paid tiers
    """
    
    def __init__(self):
        """Initialize rate limiter and ensure DB schema exists."""
        self._init_db()
    
    def _init_db(self):
        """Create necessary database tables."""
        with sqlite3.connect(DB_PATH) as conn:
            # Subscriptions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    user_id TEXT PRIMARY KEY,
                    tier TEXT NOT NULL DEFAULT 'free',
                    started_at TEXT NOT NULL,
                    expires_at TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    stripe_subscription_id TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Usage logs table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    date TEXT NOT NULL,  -- YYYY-MM-DD for daily aggregation
                    endpoint TEXT NOT NULL,
                    tokens_used INTEGER DEFAULT 0,
                    cost_cents INTEGER DEFAULT 0,  -- For custom tier
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Create index for fast lookups
            try:
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_usage_user_date 
                    ON usage_logs(user_id, date)
                """)
            except sqlite3.OperationalError:
                pass
            
            conn.commit()
    
    def get_user_tier(self, user_id: str) -> SubscriptionTier:
        """Get current subscription tier for user."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("""
                SELECT tier, expires_at, is_active 
                FROM subscriptions 
                WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            
            if not row:
                # New user - auto-assign free tier
                self._create_free_subscription(user_id)
                return SubscriptionTier.FREE
            
            tier, expires_at, is_active = row
            
            # Check if subscription expired
            if expires_at:
                expiry = datetime.fromisoformat(expires_at)
                if datetime.utcnow() > expiry:
                    # Expired - downgrade to free
                    self._downgrade_to_free(user_id)
                    return SubscriptionTier.FREE
            
            if not is_active:
                return SubscriptionTier.FREE
            
            return SubscriptionTier(tier)
    
    def get_daily_usage(self, user_id: str) -> int:
        """Get number of API calls made today by user."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) 
                FROM usage_logs 
                WHERE user_id = ? AND date = ?
            """, (user_id, today))
            
            count = cursor.fetchone()[0]
            return count
    
    def check_rate_limit(self, user_id: str) -> Tuple[bool, Dict]:
        """
        Check if user has exceeded their rate limit.
        
        Returns:
            (allowed: bool, info: dict)
            
        Info dict contains:
            - tier: Current subscription tier
            - daily_limit: Max calls per day
            - used_today: Calls made today
            - remaining: Calls remaining
            - reset_at: When limit resets
        """
        tier = self.get_user_tier(user_id)
        plan = PLANS[tier]
        used_today = self.get_daily_usage(user_id)
        remaining = max(0, plan.daily_limit - used_today)
        
        # Calculate next reset time (midnight UTC)
        now = datetime.utcnow()
        tomorrow = now + timedelta(days=1)
        reset_at = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
        
        info = {
            "tier": tier.value,
            "plan_name": plan.name,
            "daily_limit": plan.daily_limit,
            "used_today": used_today,
            "remaining": remaining,
            "reset_at": reset_at.isoformat(),
            "is_unlimited": tier == SubscriptionTier.CUSTOM
        }
        
        allowed = used_today < plan.daily_limit
        
        return allowed, info
    
    def log_usage(self, user_id: str, endpoint: str = "/api/chat", tokens: int = 0):
        """Log an API usage event."""
        now = datetime.utcnow()
        timestamp = now.isoformat()
        date = now.strftime("%Y-%m-%d")
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO usage_logs (user_id, timestamp, date, endpoint, tokens_used)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, timestamp, date, endpoint, tokens))
            conn.commit()
    
    def get_subscription_info(self, user_id: str) -> Dict:
        """Get full subscription details for user."""
        tier = self.get_user_tier(user_id)
        plan = PLANS[tier]
        used_today = self.get_daily_usage(user_id)
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("""
                SELECT started_at, expires_at, stripe_subscription_id
                FROM subscriptions
                WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            
            if row:
                started_at, expires_at, stripe_id = row
            else:
                started_at = datetime.utcnow().isoformat()
                expires_at = None
                stripe_id = None
        
        return {
            "tier": tier.value,
            "plan_name": plan.name,
            "price_monthly": plan.price_monthly,
            "daily_limit": plan.daily_limit,
            "used_today": used_today,
            "remaining": max(0, plan.daily_limit - used_today),
            "started_at": started_at,
            "expires_at": expires_at,
            "features": plan.features,
            "description": plan.description,
            "stripe_subscription_id": stripe_id
        }
    
    def upgrade_subscription(self, user_id: str, new_tier: SubscriptionTier, 
                           stripe_subscription_id: Optional[str] = None) -> bool:
        """
        Upgrade user to a new subscription tier.
        
        Args:
            user_id: User to upgrade
            new_tier: Target subscription tier
            stripe_subscription_id: Stripe subscription ID (for paid tiers)
            
        Returns:
            Success status
        """
        if new_tier not in PLANS:
            return False
        
        now = datetime.utcnow()
        started_at = now.isoformat()
        
        # Set expiry date (30 days from now for monthly plans)
        if new_tier == SubscriptionTier.FREE or new_tier == SubscriptionTier.CUSTOM:
            expires_at = None  # No expiry for free/custom
        else:
            expiry = now + timedelta(days=30)
            expires_at = expiry.isoformat()
        
        with sqlite3.connect(DB_PATH) as conn:
            # Check if subscription exists
            cursor = conn.execute("SELECT user_id FROM subscriptions WHERE user_id = ?", (user_id,))
            exists = cursor.fetchone() is not None
            
            if exists:
                # Update existing subscription
                conn.execute("""
                    UPDATE subscriptions 
                    SET tier = ?, started_at = ?, expires_at = ?, 
                        is_active = 1, stripe_subscription_id = ?
                    WHERE user_id = ?
                """, (new_tier.value, started_at, expires_at, stripe_subscription_id, user_id))
            else:
                # Create new subscription
                conn.execute("""
                    INSERT INTO subscriptions (user_id, tier, started_at, expires_at, stripe_subscription_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, new_tier.value, started_at, expires_at, stripe_subscription_id))
            
            conn.commit()
        
        return True
    
    def cancel_subscription(self, user_id: str) -> bool:
        """Cancel subscription and downgrade to free tier."""
        return self._downgrade_to_free(user_id)
    
    def _create_free_subscription(self, user_id: str):
        """Create a free tier subscription for new user."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT OR IGNORE INTO subscriptions (user_id, tier, started_at, is_active)
                VALUES (?, 'free', ?, 1)
            """, (user_id, datetime.utcnow().isoformat()))
            conn.commit()
    
    def _downgrade_to_free(self, user_id: str):
        """Downgrade user to free tier."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                UPDATE subscriptions 
                SET tier = 'free', is_active = 1, expires_at = NULL
                WHERE user_id = ?
            """, (user_id,))
            conn.commit()
        return True
    
    @staticmethod
    def get_all_plans() -> Dict[str, Dict]:
        """Get all available subscription plans."""
        return {
            tier.value: {
                "tier": tier.value,
                "name": plan.name,
                "price_monthly": plan.price_monthly,
                "daily_limit": plan.daily_limit,
                "description": plan.description,
                "features": plan.features
            }
            for tier, plan in PLANS.items()
        }


# Singleton instance
rate_limiter = RateLimiter()
