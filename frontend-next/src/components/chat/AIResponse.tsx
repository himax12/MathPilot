"use client";

import { motion } from "framer-motion";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import RefreshIcon from "@mui/icons-material/Refresh";
import MathRenderer from "../rendering/MathRenderer";

interface AIResponseProps {
  content: string;
  onCopy?: () => void;
  onRetry?: () => void;
}

/**
 * AIResponse: AI message display with rich content
 * 
 * Supports markdown, LaTeX math, code blocks
 * Action buttons for copy and retry
 */
export default function AIResponse({ content, onCopy, onRetry }: AIResponseProps) {
  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    onCopy?.();
  };

  return (
    <div className="flex items-start gap-3">
      {/* AI Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center shrink-0">
        <span className="text-sm">π</span>
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="bg-[#1a1a1a] rounded-2xl rounded-tl-md px-4 py-3 border border-[#2a2a2a]">
          <MathRenderer content={content} />
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2 mt-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleCopy}
            className="flex items-center gap-1 px-3 py-1 text-xs text-gray-400 hover:text-white rounded-md hover:bg-[#2a2a2a] transition-colors"
          >
            <ContentCopyIcon style={{ fontSize: 14 }} />
            Copy
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onRetry}
            className="flex items-center gap-1 px-3 py-1 text-xs text-gray-400 hover:text-white rounded-md hover:bg-[#2a2a2a] transition-colors"
          >
            <RefreshIcon style={{ fontSize: 14 }} />
            Try again
          </motion.button>
        </div>
      </div>
    </div>
  );
}
