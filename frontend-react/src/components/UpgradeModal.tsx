/**
 * UpgradeModal Component
 *
 * Beautiful modal showing subscription tiers with pricing and features.
 * Allows users to select and upgrade to a higher tier.
 */

import { useEffect, useState } from "react";
import { X, Check, Zap, Star, Crown, Infinity } from "lucide-react";
import { apiClient } from "../lib/api";

interface Plan {
  tier: string;
  name: string;
  price_monthly: number;
  daily_limit: number;
  description: string;
  features: string[];
}

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentTier?: string;
  onUpgradeSuccess?: () => void;
}

const TIER_ICONS = {
  free: Zap,
  standard: Star,
  pro: Crown,
  premium: Crown,
  custom: Infinity,
};

const TIER_COLORS = {
  free: "from-gray-600 to-gray-700",
  standard: "from-blue-600 to-cyan-600",
  pro: "from-purple-600 to-pink-600",
  premium: "from-amber-500 to-orange-600",
  custom: "from-emerald-600 to-teal-600",
};

export function UpgradeModal({
  isOpen,
  onClose,
  currentTier = "free",
  onUpgradeSuccess,
}: UpgradeModalProps) {
  const [plans, setPlans] = useState<Record<string, Plan>>({});
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(false);
  const [selectedTier, setSelectedTier] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      fetchPlans();
    }
  }, [isOpen]);

  const fetchPlans = async () => {
    try {
      const response = await apiClient.get("/api/billing/plans");
      setPlans(response.data);
    } catch (error) {
      console.error("Failed to fetch plans:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = async (tier: string) => {
    setUpgrading(true);
    setSelectedTier(tier);

    try {
      const response = await apiClient.post("/api/billing/upgrade", { tier });

      if (response.data.success) {
        // Show success message
        alert(
          `✅ Successfully upgraded to ${response.data.subscription.plan_name}!`,
        );
        onUpgradeSuccess?.();
        onClose();
      }
    } catch (error: any) {
      console.error("Upgrade failed:", error);
      alert(
        `❌ Upgrade failed: ${error.response?.data?.detail || error.message}`,
      );
    } finally {
      setUpgrading(false);
      setSelectedTier(null);
    }
  };

  if (!isOpen) return null;

  const plansArray = Object.values(plans);
  const sortedPlans = plansArray.sort(
    (a, b) => a.price_monthly - b.price_monthly,
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <div className="bg-gray-900 rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto border border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-gray-900 border-b border-gray-700 p-6 flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-white">Choose Your Plan</h2>
            <p className="text-gray-400 mt-1">
              Upgrade to unlock more solving power
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-800 transition-colors text-gray-400 hover:text-white"
          >
            <X size={24} />
          </button>
        </div>

        {/* Plans Grid */}
        <div className="p-6">
          {loading ? (
            <div className="text-center py-12 text-gray-400">
              Loading plans...
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sortedPlans.map((plan) => {
                const Icon =
                  TIER_ICONS[plan.tier as keyof typeof TIER_ICONS] || Star;
                const gradient =
                  TIER_COLORS[plan.tier as keyof typeof TIER_COLORS] ||
                  "from-gray-600 to-gray-700";
                const isCurrent = plan.tier === currentTier;
                const isUpgrade =
                  !isCurrent &&
                  plan.price_monthly > (plans[currentTier]?.price_monthly || 0);
                const isRecommended = plan.tier === "pro";
                const isUpgrading = upgrading && selectedTier === plan.tier;

                return (
                  <div
                    key={plan.tier}
                    className={`relative rounded-xl border-2 overflow-hidden transition-all ${
                      isCurrent
                        ? "border-green-500 bg-green-500/5"
                        : isRecommended
                          ? "border-purple-500 bg-purple-500/5 scale-105"
                          : "border-gray-700 bg-gray-800/50 hover:border-gray-600"
                    }`}
                  >
                    {/* Recommended Badge */}
                    {isRecommended && !isCurrent && (
                      <div className="absolute top-0 right-0 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                        MOST POPULAR
                      </div>
                    )}

                    {/* Current Badge */}
                    {isCurrent && (
                      <div className="absolute top-0 right-0 bg-green-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                        CURRENT PLAN
                      </div>
                    )}

                    <div className="p-6">
                      {/* Icon & Name */}
                      <div className="flex items-center gap-3 mb-4">
                        <div
                          className={`p-3 rounded-lg bg-gradient-to-br ${gradient}`}
                        >
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-white">
                            {plan.name}
                          </h3>
                          <p className="text-sm text-gray-400">
                            {plan.tier.toUpperCase()}
                          </p>
                        </div>
                      </div>

                      {/* Price */}
                      <div className="mb-4">
                        {plan.price_monthly === 0 && plan.tier === "free" ? (
                          <div className="text-3xl font-bold text-white">
                            Free
                          </div>
                        ) : plan.tier === "custom" ? (
                          <div>
                            <div className="text-2xl font-bold text-white">
                              $20
                            </div>
                            <div className="text-sm text-gray-400">
                              per 100 requests
                            </div>
                          </div>
                        ) : (
                          <div>
                            <div className="text-3xl font-bold text-white">
                              ${plan.price_monthly}
                              <span className="text-lg text-gray-400">
                                /month
                              </span>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Daily Limit */}
                      <div className="mb-4 pb-4 border-b border-gray-700">
                        {plan.tier === "custom" ? (
                          <div className="text-gray-300 flex items-center gap-2">
                            <Infinity size={20} />
                            <span className="font-medium">
                              Unlimited daily requests
                            </span>
                          </div>
                        ) : (
                          <div className="text-gray-300">
                            <span className="text-2xl font-bold text-white">
                              {plan.daily_limit}
                            </span>
                            <span className="text-sm"> problems per day</span>
                          </div>
                        )}
                      </div>

                      {/* Description */}
                      <p className="text-gray-400 text-sm mb-4">
                        {plan.description}
                      </p>

                      {/* Features */}
                      <ul className="space-y-2 mb-6">
                        {plan.features.map((feature, idx) => (
                          <li
                            key={idx}
                            className="flex items-start gap-2 text-sm text-gray-300"
                          >
                            <Check
                              size={16}
                              className="text-green-500 mt-0.5 flex-shrink-0"
                            />
                            <span>{feature}</span>
                          </li>
                        ))}
                      </ul>

                      {/* Action Button */}
                      {isCurrent ? (
                        <button
                          disabled
                          className="w-full py-3 rounded-lg bg-green-600 text-white font-medium cursor-not-allowed opacity-75"
                        >
                          Current Plan
                        </button>
                      ) : isUpgrade ? (
                        <button
                          onClick={() => handleUpgrade(plan.tier)}
                          disabled={upgrading}
                          className={`w-full py-3 rounded-lg bg-gradient-to-r ${gradient} text-white font-medium hover:opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed`}
                        >
                          {isUpgrading
                            ? "Upgrading..."
                            : `Upgrade to ${plan.name}`}
                        </button>
                      ) : (
                        <button
                          disabled
                          className="w-full py-3 rounded-lg bg-gray-700 text-gray-400 font-medium cursor-not-allowed"
                        >
                          Lower Tier
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer Note */}
        <div className="border-t border-gray-700 p-6 bg-gray-800/50">
          <p className="text-sm text-gray-400 text-center">
            💡 <strong>Note:</strong> This is a demo implementation. In
            production, this would integrate with Stripe for secure payment
            processing. All upgrades are instant for testing purposes.
          </p>
        </div>
      </div>
    </div>
  );
}
