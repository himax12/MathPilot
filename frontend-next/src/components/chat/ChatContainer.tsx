"use client";

import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import MessageList from "./MessageList";
import InputBar from "../input/InputBar";
import EditIcon from "@mui/icons-material/Edit";
import ShareIcon from "@mui/icons-material/Share";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import api from "@/lib/api";
import { useSimulatedStreaming } from "@/hooks/useStreaming";

export interface Message {
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

/**
 * ChatContainer: The brain of the chat UI
 * 
 * Now with real-time streaming support!
 * Falls back to simulated streaming when backend is unavailable
 */
export default function ChatContainer() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatTitle, setChatTitle] = useState("Math Helper");
  const [streamingMessageId, setStreamingMessageId] = useState<string | null>(null);
  
  const { startStream: startSimulatedStream, stopStream: stopSimulatedStream } = useSimulatedStreaming();

  // Update streaming message content
  const updateStreamingMessage = useCallback((messageId: string, chunk: string) => {
    setMessages((prev) =>
      prev.map((m) =>
        m.id === messageId ? { ...m, content: m.content + chunk } : m
      )
    );
  }, []);

  // Complete streaming
  const completeStreaming = useCallback((messageId: string) => {
    setMessages((prev) =>
      prev.map((m) =>
        m.id === messageId ? { ...m, isStreaming: false } : m
      )
    );
    setStreamingMessageId(null);
    setIsLoading(false);
  }, []);

  // Stop streaming
  const handleStopStreaming = useCallback(() => {
    stopSimulatedStream();
    if (streamingMessageId) {
      completeStreaming(streamingMessageId);
    }
  }, [stopSimulatedStream, streamingMessageId, completeStreaming]);

  const handleSendMessage = async (
    content: string,
    mode: string,
    image?: { file: File; preview: string }
  ) => {
    if (!content.trim() && !image) return;

    // Build user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: content.trim() || "Solve this problem from the image",
      timestamp: new Date(),
      attachments: image
        ? [{ type: "image", url: image.preview, name: image.file.name }]
        : undefined,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Update chat title from first message
    if (messages.length === 0) {
      const title = content.slice(0, 40) || "Image problem";
      setChatTitle(title + (content.length > 40 ? "..." : ""));
    }

    // Create AI message placeholder for streaming
    const aiMessageId = (Date.now() + 1).toString();
    const aiMessage: Message = {
      id: aiMessageId,
      role: "assistant",
      content: "",
      timestamp: new Date(),
      isStreaming: true,
    };
    setMessages((prev) => [...prev, aiMessage]);
    setStreamingMessageId(aiMessageId);

    try {
      // Prepare image for API if attached
      let imageBase64: string | undefined;
      if (image) {
        imageBase64 = image.preview.split(",")[1];
      }

      // Try real API first
      const response = await api.solve({
        problem: content,
        mode: mode as "solve" | "explain" | "practice" | "graph",
        image: imageBase64,
      });

      if (response.success && response.solution) {
        // Stream the response for a nice effect
        startSimulatedStream(response.solution, {
          onChunk: (chunk) => updateStreamingMessage(aiMessageId, chunk),
          onComplete: () => completeStreaming(aiMessageId),
          onError: () => completeStreaming(aiMessageId),
        });
      } else {
        // Use mock response with streaming
        const mockContent = generateMockResponse(content, mode, !!image);
        startSimulatedStream(mockContent, {
          onChunk: (chunk) => updateStreamingMessage(aiMessageId, chunk),
          onComplete: () => completeStreaming(aiMessageId),
          onError: () => completeStreaming(aiMessageId),
        });
      }
    } catch (error) {
      console.error("API error:", error);
      // Stream mock response as fallback
      const mockContent = generateMockResponse(content, mode, !!image);
      startSimulatedStream(mockContent, {
        onChunk: (chunk) => updateStreamingMessage(aiMessageId, chunk),
        onComplete: () => completeStreaming(aiMessageId),
        onError: () => completeStreaming(aiMessageId),
      });
    }
  };

  const handleRetry = useCallback((messageId: string) => {
    // Find the user message before this AI message
    const messageIndex = messages.findIndex((m) => m.id === messageId);
    if (messageIndex > 0) {
      const userMessage = messages[messageIndex - 1];
      if (userMessage.role === "user") {
        // Remove the AI message and resend
        setMessages((prev) => prev.filter((m) => m.id !== messageId));
        handleSendMessage(userMessage.content, "solve");
      }
    }
  }, [messages]);

  return (
    <div className="flex-1 flex flex-col h-full">
      {/* Header */}
      <header className="h-14 border-b border-[#2a2a2a] flex items-center justify-between px-4 shrink-0">
        <div className="flex items-center gap-2">
          <span className="text-lg">💬</span>
          <h1 className="text-white font-medium">{chatTitle}</h1>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="text-gray-500 hover:text-white ml-1 p-1"
          >
            <EditIcon style={{ fontSize: 16 }} />
          </motion.button>
        </div>
        <div className="flex items-center gap-1">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="text-gray-400 hover:text-white px-3 py-1.5 rounded-lg hover:bg-[#2a2a2a] flex items-center gap-2 transition-colors"
          >
            <ShareIcon style={{ fontSize: 16 }} />
            Share
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-[#2a2a2a] transition-colors"
          >
            <MoreHorizIcon style={{ fontSize: 20 }} />
          </motion.button>
        </div>
      </header>

      {/* Messages with streaming support */}
      <MessageList 
        messages={messages} 
        isLoading={isLoading && !streamingMessageId}
        onStopStreaming={handleStopStreaming}
        onRetry={handleRetry}
      />

      {/* Input */}
      <InputBar onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}

// Mock response generator (fallback when API is unavailable)
function generateMockResponse(userInput: string, mode: string, hasImage: boolean): string {
  if (hasImage) {
    return `I've analyzed the image you uploaded.

**Step 1:** Identify the problem
I can see a mathematical equation or expression in the image.

**Step 2:** Extract the content
$$x^2 + 5x + 6 = 0$$

**Step 3:** Solve step by step
Using factoring method:
$$(x + 2)(x + 3) = 0$$

**Answer:**
$$x = -2 \\text{ or } x = -3$$

*Note: This is a demo response. Connect to the backend for actual OCR and solving.*`;
  }

  const responses: Record<string, string> = {
    solve: `Let me solve this step by step!

**Step 1:** Identify the equation
$$${userInput.includes("=") ? userInput.replace(/\^/g, "^") : "x^2 + 5x + 6 = 0"}$$

**Step 2:** Apply the appropriate method
Using the quadratic formula or factoring...

**Step 3:** Simplify and solve
$$(x + 2)(x + 3) = 0$$

**Answer:**
$$x = -2 \\text{ or } x = -3$$`,
    explain: `Great question! Let me explain this concept...

The key idea here is understanding how mathematical operations work together. 

When we look at **${userInput}**, we're essentially dealing with a **polynomial equation**. 

The fundamental theorem of algebra tells us that a polynomial of degree n has exactly n roots (counting multiplicity).

For quadratic equations like $ax^2 + bx + c = 0$, we have several solving methods:
1. **Factoring** - Find two numbers that multiply to give $c$ and add to give $b$
2. **Quadratic Formula** - $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$
3. **Completing the Square** - Rewrite as $(x+p)^2 = q$`,
    practice: `Here's a practice problem for you!

**Problem:** Solve for $x$
$$2x^2 - 8x + 6 = 0$$

**Difficulty:** ⭐⭐ Medium

**Hints available:**
1. Try factoring out the GCF first
2. Use the quadratic formula if factoring doesn't work

Take your time and try different approaches!`,
    graph: `I'll help you visualize this function!

For **${userInput || "y = x^2 + 5x + 6"}**, here's the analysis:

📈 **Key Features:**
- **Type:** Parabola (quadratic function)
- **Opens:** Upward (coefficient of $x^2$ is positive)
- **Vertex:** $\\left(-\\frac{5}{2}, -\\frac{1}{4}\\right)$
- **Y-intercept:** $(0, 6)$
- **X-intercepts:** $(-2, 0)$ and $(-3, 0)$

**Domain:** All real numbers $(-\\infty, \\infty)$
**Range:** $\\left[-\\frac{1}{4}, \\infty\\right)$`,
  };

  return responses[mode] || responses.solve;
}
