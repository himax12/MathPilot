"""
Test rate limiter with updated limits.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rate_limiter import RateLimiter, SubscriptionTier, PLANS

def test_free_tier_limit():
    """Test that FREE tier has 10 prompts per day."""
    rate_limiter = RateLimiter()
    
    # Check plan configuration
    free_plan = PLANS[SubscriptionTier.FREE]
    assert free_plan.daily_limit == 10, f"Expected FREE tier to have 10 daily limit, got {free_plan.daily_limit}"
    print("✅ FREE tier configured for 10 prompts/day")
    
def test_standard_tier_limit():
    """Test that STANDARD tier has 25 prompts per day."""
    standard_plan = PLANS[SubscriptionTier.STANDARD]
    assert standard_plan.daily_limit == 25, f"Expected STANDARD tier to have 25 daily limit, got {standard_plan.daily_limit}"
    print("✅ STANDARD tier configured for 25 prompts/day")

def test_rate_limit_check():
    """Test rate limit checking for a test user."""
    rate_limiter = RateLimiter()
    test_user_id = "test_user_rate_limit_check"
    
    # Check initial state
    allowed, info = rate_limiter.check_rate_limit(test_user_id)
    print(f"✅ Test user initial status: {info['used_today']}/{info['daily_limit']} (tier: {info['tier']})")
    
    # Verify free tier gets 10 limit
    assert info['daily_limit'] == 10, f"Expected daily limit of 10 for test user, got {info['daily_limit']}"
    print("✅ Rate limit check working correctly")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Rate Limiter with Updated Limits")
    print("=" * 60)
    
    test_free_tier_limit()
    test_standard_tier_limit()
    test_rate_limit_check()
    
    print("\n" + "=" * 60)
    print("✅ All rate limiter tests passed!")
    print("=" * 60)
