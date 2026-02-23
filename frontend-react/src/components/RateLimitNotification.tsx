/**
 * RateLimitNotification Component
 *
 * Beautiful notification shown when user hits rate limit.
 * Displays current usage and prompts to upgrade.
 */

import { AlertTriangle, Zap } from "lucide-react";

interface RateLimitNotificationProps {
  limitInfo: {
    tier: string;
    plan_name: string;
    daily_limit: number;
    used_today: number;
    remaining: number;
    reset_at: string;
  };
  onUpgradeClick: () => void;
  onDismiss: () => void;
}

export function RateLimitNotification({
  limitInfo,
  onUpgradeClick,
  onDismiss,
}: RateLimitNotificationProps) {
  const resetDate = new Date(limitInfo.reset_at);
  const hoursUntilReset = Math.ceil(
    (resetDate.getTime() - Date.now()) / (1000 * 60 * 60),
  );

  return (
    <div className="fixed top-4 right-4 z-50 max-w-md animate-in slide-in-from-top-5">
      <div className="bg-gradient-to-br from-red-900 to-orange-900 border-2 border-red-500 rounded-xl shadow-2xl p-6">
        {/* Header */}
        <div className="flex items-start gap-4 mb-4">
          <div className="p-3 bg-red-500 rounded-lg">
            <AlertTriangle className="w-6 h-6 text-white" />
          </div>

          <div className="flex-1">
            <h3 className="text-xl font-bold text-white mb-1">
              Daily Limit Reached
            </h3>
            <p className="text-red-200 text-sm">
              You've used all {limitInfo.daily_limit} prompts for today
            </p>
          </div>

          <button
            onClick={onDismiss}
            className="p-1 hover:bg-red-800 rounded transition-colors text-red-200 hover:text-white"
          >
            ✕
          </button>
        </div>

        {/* Stats */}
        <div className="bg-black/30 rounded-lg p-4 mb-4">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <div className="text-3xl font-bold text-white">
                {limitInfo.used_today}
              </div>
              <div className="text-xs text-red-200">Used Today</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">
                {hoursUntilReset}h
              </div>
              <div className="text-xs text-red-200">Until Reset</div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="space-y-3">
          <p className="text-white text-sm">
            Want to keep solving? Upgrade to get more prompts per day!
          </p>

          <button
            onClick={onUpgradeClick}
            className="w-full py-3 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 text-white font-medium hover:from-purple-700 hover:to-pink-700 transition-all hover:shadow-xl hover:scale-105 flex items-center justify-center gap-2"
          >
            <Zap className="w-5 h-5" />
            <span>View Upgrade Options</span>
          </button>

          <p className="text-xs text-red-200 text-center">
            Or wait until {resetDate.toLocaleTimeString()} for your daily limit
            to reset
          </p>
        </div>
      </div>
    </div>
  );
}
