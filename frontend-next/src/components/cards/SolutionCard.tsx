"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import MathRenderer from "../rendering/MathRenderer";

interface SolutionStep {
  stepNumber: number;
  title: string;
  content: string;
  explanation?: string;
}

interface SolutionCardProps {
  steps: SolutionStep[];
}

/**
 * SolutionCard: Expandable step-by-step solution display
 * 
 * Shows numbered steps with math rendering
 * Each step can be expanded for more details
 */
export default function SolutionCard({ steps }: SolutionCardProps) {
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set([0]));

  const toggleStep = (stepNumber: number) => {
    setExpandedSteps((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(stepNumber)) {
        newSet.delete(stepNumber);
      } else {
        newSet.add(stepNumber);
      }
      return newSet;
    });
  };

  const expandAll = () => {
    setExpandedSteps(new Set(steps.map((_, i) => i)));
  };

  const collapseAll = () => {
    setExpandedSteps(new Set());
  };

  return (
    <div className="space-y-3">
      {/* Controls */}
      <div className="flex justify-end gap-2">
        <button
          onClick={expandAll}
          className="text-xs text-gray-400 hover:text-white transition-colors"
        >
          Expand all
        </button>
        <span className="text-gray-500">|</span>
        <button
          onClick={collapseAll}
          className="text-xs text-gray-400 hover:text-white transition-colors"
        >
          Collapse all
        </button>
      </div>

      {/* Steps */}
      <div className="space-y-2">
        {steps.map((step, index) => {
          const isExpanded = expandedSteps.has(index);

          return (
            <motion.div
              key={step.stepNumber}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-[#0a0a0a] border border-[#2a2a2a] rounded-xl overflow-hidden"
            >
              {/* Step Header */}
              <button
                onClick={() => toggleStep(index)}
                className="w-full px-4 py-3 flex items-center gap-3 hover:bg-[#141414] transition-colors"
              >
                <div className="w-7 h-7 rounded-full bg-[#4ADE80]/20 text-[#4ADE80] flex items-center justify-center text-sm font-medium">
                  {step.stepNumber}
                </div>
                <span className="flex-1 text-left text-white font-medium">
                  {step.title}
                </span>
                <CheckCircleIcon 
                  className="text-[#4ADE80]" 
                  style={{ fontSize: 18 }} 
                />
                {isExpanded ? (
                  <ExpandLessIcon className="text-gray-400" style={{ fontSize: 20 }} />
                ) : (
                  <ExpandMoreIcon className="text-gray-400" style={{ fontSize: 20 }} />
                )}
              </button>

              {/* Step Content */}
              <AnimatePresence>
                {isExpanded && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                    className="overflow-hidden"
                  >
                    <div className="px-4 pb-4 pt-2 border-t border-[#2a2a2a]">
                      {/* Math Content */}
                      <div className="bg-[#141414] rounded-lg p-3 mb-2">
                        <MathRenderer content={step.content} />
                      </div>

                      {/* Explanation */}
                      {step.explanation && (
                        <p className="text-gray-400 text-sm leading-relaxed">
                          {step.explanation}
                        </p>
                      )}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// Helper to parse solution text into steps
export function parseSolutionSteps(content: string): SolutionStep[] {
  const stepRegex = /\*\*Step (\d+):\*\*\s*([^\n]+)\n([\s\S]*?)(?=\*\*Step \d+:|$)/g;
  const steps: SolutionStep[] = [];
  
  let match;
  while ((match = stepRegex.exec(content)) !== null) {
    steps.push({
      stepNumber: parseInt(match[1]),
      title: match[2].trim(),
      content: match[3].trim(),
    });
  }

  return steps;
}
