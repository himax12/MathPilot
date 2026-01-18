"use client";

import { useCallback, useRef, useState } from "react";

interface StreamingOptions {
  onChunk: (chunk: string) => void;
  onComplete: () => void;
  onError: (error: string) => void;
}

/**
 * useStreaming Hook
 * 
 * Handles real-time streaming of AI responses using:
 * 1. Server-Sent Events (SSE) - Primary method
 * 2. Fetch with ReadableStream - Fallback
 * 
 * Usage:
 * const { startStream, stopStream, isStreaming } = useStreaming();
 * startStream(prompt, mode, { onChunk, onComplete, onError });
 */
export function useStreaming() {
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  const stopStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const startStreamSSE = useCallback(
    (prompt: string, mode: string, options: StreamingOptions, imageBase64?: string) => {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      
      // Build query params
      const params = new URLSearchParams({
        problem: prompt,
        mode: mode,
      });
      if (imageBase64) {
        params.append("image", imageBase64);
      }

      const eventSource = new EventSource(`${baseUrl}/api/solve/stream?${params}`);
      eventSourceRef.current = eventSource;
      setIsStreaming(true);

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "chunk") {
            options.onChunk(data.content);
          } else if (data.type === "complete") {
            options.onComplete();
            stopStream();
          } else if (data.type === "error") {
            options.onError(data.message);
            stopStream();
          }
        } catch {
          // Plain text chunk
          options.onChunk(event.data);
        }
      };

      eventSource.onerror = () => {
        // SSE failed, fall back to fetch streaming
        eventSource.close();
        startStreamFetch(prompt, mode, options, imageBase64);
      };
    },
    [stopStream]
  );

  const startStreamFetch = useCallback(
    async (prompt: string, mode: string, options: StreamingOptions, imageBase64?: string) => {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const abortController = new AbortController();
      abortControllerRef.current = abortController;
      setIsStreaming(true);

      try {
        const response = await fetch(`${baseUrl}/api/solve/stream`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            problem: prompt,
            mode: mode,
            image: imageBase64,
          }),
          signal: abortController.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error("No readable stream");
        }

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          
          // Handle SSE format or plain text
          const lines = chunk.split("\n");
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.type === "chunk") {
                  options.onChunk(data.content);
                } else if (data.type === "complete") {
                  options.onComplete();
                  stopStream();
                  return;
                }
              } catch {
                options.onChunk(line.slice(6));
              }
            } else if (line.trim()) {
              options.onChunk(line);
            }
          }
        }

        options.onComplete();
      } catch (error) {
        if ((error as Error).name !== "AbortError") {
          options.onError((error as Error).message);
        }
      } finally {
        setIsStreaming(false);
      }
    },
    [stopStream]
  );

  const startStream = useCallback(
    (prompt: string, mode: string, options: StreamingOptions, imageBase64?: string) => {
      // Try SSE first for GET requests, fall back to fetch for POST
      if (!imageBase64 && typeof EventSource !== "undefined") {
        startStreamSSE(prompt, mode, options);
      } else {
        startStreamFetch(prompt, mode, options, imageBase64);
      }
    },
    [startStreamSSE, startStreamFetch]
  );

  return {
    startStream,
    stopStream,
    isStreaming,
  };
}

/**
 * Simulated streaming for demo/fallback mode
 * 
 * Streams text character by character with realistic timing
 */
export function useSimulatedStreaming() {
  const [isStreaming, setIsStreaming] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const stopStream = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const startStream = useCallback(
    (fullText: string, options: StreamingOptions) => {
      setIsStreaming(true);
      let index = 0;
      
      const streamNextChunk = () => {
        if (index >= fullText.length) {
          options.onComplete();
          setIsStreaming(false);
          return;
        }

        // Stream 1-5 characters at a time for realistic effect
        const chunkSize = Math.min(
          Math.floor(Math.random() * 4) + 1,
          fullText.length - index
        );
        const chunk = fullText.slice(index, index + chunkSize);
        options.onChunk(chunk);
        index += chunkSize;

        // Variable delay for natural feel (10-50ms per chunk)
        const delay = Math.random() * 40 + 10;
        timeoutRef.current = setTimeout(streamNextChunk, delay);
      };

      streamNextChunk();
    },
    []
  );

  return {
    startStream,
    stopStream,
    isStreaming,
  };
}

export default useStreaming;
