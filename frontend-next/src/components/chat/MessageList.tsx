"use client";

import { useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import MessageBubble from "./MessageBubble";
import StreamingAIResponse from "./StreamingAIResponse";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
  attachments?: {
    type: "image" | "file";
    url: string;
    name: string;
  }[];
}

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  onStopStreaming?: () => void;
  onRetry?: (messageId: string) => void;
}

/**
 * MessageList: Scrollable container with streaming support
 * 
 * Auto-scrolls during streaming
 * Shows blinking cursor while response is generating
 */
export default function MessageList({ 
  messages, 
  isLoading,
  onStopStreaming,
  onRetry,
}: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive or during streaming
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Check if any message is streaming
  const hasStreamingMessage = messages.some((m) => m.isStreaming);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto px-4 py-6 space-y-6"
    >
      {/* Empty State */}
      {messages.length === 0 && !isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="h-full flex flex-col items-center justify-center text-center"
        >
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center mb-6">
            <span className="text-4xl">π</span>
          </div>
          <h2 className="text-2xl font-semibold text-white mb-2">
            Hi! I'm Math Mentor
          </h2>
          <p className="text-gray-400 max-w-md mb-8">
            I can help you solve equations, understand concepts, practice problems, and visualize graphs.
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {[
              "Solve x² + 5x + 6 = 0",
              "Explain derivatives",
              "Graph y = sin(x)",
              "Upload a problem image",
            ].map((suggestion) => (
              <button
                key={suggestion}
                className="px-4 py-2 rounded-full bg-[#1a1a1a] border border-[#2a2a2a] text-gray-300 text-sm hover:bg-[#2a2a2a] hover:text-white transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </motion.div>
      )}

      {/* Messages */}
      <AnimatePresence mode="popLayout">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {message.role === "user" ? (
              <MessageBubble
                content={message.content}
                timestamp={message.timestamp}
                attachments={message.attachments}
              />
            ) : (
              <StreamingAIResponse
                content={message.content}
                isStreaming={message.isStreaming}
                onStop={onStopStreaming}
                onRetry={() => onRetry?.(message.id)}
              />
            )}
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Loading Indicator (only when not streaming) */}
      {isLoading && !hasStreamingMessage && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-start gap-3"
        >
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center shrink-0">
            <span className="text-sm">π</span>
          </div>
          <div className="flex gap-1 items-center h-8">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
              className="w-2 h-2 bg-gray-400 rounded-full"
            />
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
              className="w-2 h-2 bg-gray-400 rounded-full"
            />
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
              className="w-2 h-2 bg-gray-400 rounded-full"
            />
          </div>
        </motion.div>
      )}
    </div>
  );
}
