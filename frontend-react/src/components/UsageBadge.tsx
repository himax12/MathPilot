/**
 * UsageBadge Component
 *
 * Displays current API usage and daily limit in a compact badge.
 * Shows upgrade prompt when user is approaching or has hit their limit.
 */

import { useEffect, useState } from "react";
import { apiClient } from "../lib/api";

interface UsageInfo {
  allowed: boolean;
  limit_info: {
    tier: string;
    plan_name: string;
    daily_limit: number;
    used_today: number;
    remaining: number;
    reset_at: string;
    is_unlimited: boolean;
  };
  subscription: {
    tier: string;
    plan_name: string;
    price_monthly: number;
    features: string[];
  };
}

interface UsageBadgeProps {
  onUpgradeClick?: () => void;
}

export function UsageBadge({ onUpgradeClick }: UsageBadgeProps) {
  const [usage, setUsage] = useState<UsageInfo | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUsage = async () => {
    try {
      const response = await apiClient.get("/api/billing/usage");
      setUsage(response.data);
    } catch (error) {
      console.error("Failed to fetch usage:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsage();
    // Refresh usage every 30 seconds
    const interval = setInterval(fetchUsage, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading || !usage) {
    return (
      <div className="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-400 text-sm animate-pulse">
        Loading...
      </div>
    );
  }

  const { limit_info } = usage;
  const percentage = (limit_info.used_today / limit_info.daily_limit) * 100;

  // Color based on usage
  let badgeColor = "bg-green-900 text-green-200 border-green-700";
  if (percentage >= 80) {
    badgeColor = "bg-red-900 text-red-200 border-red-700";
  } else if (percentage >= 60) {
    badgeColor = "bg-yellow-900 text-yellow-200 border-yellow-700";
  }

  const isFree = limit_info.tier === "free";
  const isNearLimit = percentage >= 80;

  return (
    <div className="flex items-center gap-2">
      {/* Usage Badge */}
      <div
        className={`px-3 py-1.5 rounded-lg border ${badgeColor} text-sm font-medium flex items-center gap-2`}
      >
        {limit_info.is_unlimited ? (
          <>
            <span>∞</span>
            <span>Unlimited</span>
          </>
        ) : (
          <>
            <span>{limit_info.remaining}</span>
            <span>/</span>
            <span>{limit_info.daily_limit}</span>
            <span className="text-xs opacity-75">left today</span>
          </>
        )}
      </div>

      {/* Upgrade Button (show if free or near limit for paid users) */}
      {(isFree || (isNearLimit && !limit_info.is_unlimited)) && (
        <button
          onClick={onUpgradeClick}
          className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 text-white text-sm font-medium hover:from-purple-700 hover:to-pink-700 transition-all hover:shadow-lg hover:scale-105"
        >
          {isFree ? "⚡ Upgrade" : "📈 Get More"}
        </button>
      )}
    </div>
  );
}
