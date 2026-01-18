"use client";

import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import RefreshIcon from "@mui/icons-material/Refresh";
import StopIcon from "@mui/icons-material/Stop";
import MathRenderer from "../rendering/MathRenderer";

interface StreamingAIResponseProps {
  content: string;
  isStreaming?: boolean;
  onStop?: () => void;
  onCopy?: () => void;
  onRetry?: () => void;
}

/**
 * StreamingAIResponse: AI message with typewriter effect
 * 
 * Shows content as it streams in with a blinking cursor
 * Supports stop, copy, and retry actions
 */
export default function StreamingAIResponse({
  content,
  isStreaming = false,
  onStop,
  onCopy,
  onRetry,
}: StreamingAIResponseProps) {
  const [copied, setCopied] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // Auto-scroll during streaming
  useEffect(() => {
    if (isStreaming && contentRef.current) {
      contentRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }, [content, isStreaming]);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
    onCopy?.();
  };

  return (
    <div className="flex items-start gap-3">
      {/* AI Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center shrink-0">
        <span className="text-sm">π</span>
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0" ref={contentRef}>
        <div className="bg-[#1a1a1a] rounded-2xl rounded-tl-md px-4 py-3 border border-[#2a2a2a]">
          <div className="relative">
            <MathRenderer content={content} />
            
            {/* Blinking cursor during streaming */}
            {isStreaming && (
              <motion.span
                animate={{ opacity: [1, 0] }}
                transition={{ duration: 0.5, repeat: Infinity }}
                className="inline-block w-2 h-5 bg-[#4ADE80] ml-1 align-middle"
              />
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2 mt-2">
          {isStreaming ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={onStop}
              className="flex items-center gap-1 px-3 py-1 text-xs text-red-400 hover:text-red-300 rounded-md hover:bg-red-400/10 transition-colors"
            >
              <StopIcon style={{ fontSize: 14 }} />
              Stop
            </motion.button>
          ) : (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleCopy}
                className="flex items-center gap-1 px-3 py-1 text-xs text-gray-400 hover:text-white rounded-md hover:bg-[#2a2a2a] transition-colors"
              >
                <ContentCopyIcon style={{ fontSize: 14 }} />
                {copied ? "Copied!" : "Copy"}
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
            </>
          )}
        </div>
      </div>
    </div>
  );
}
