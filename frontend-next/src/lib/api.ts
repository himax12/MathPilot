/**
 * API Client for Math Mentor Backend
 * 
 * Handles all communication with the Python backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface SolveRequest {
  problem: string;
  mode: "solve" | "explain" | "practice" | "graph";
  image?: string; // Base64 encoded image
}

export interface SolveResponse {
  success: boolean;
  solution: string;
  steps?: {
    stepNumber: number;
    title: string;
    content: string;
    explanation?: string;
  }[];
  graph?: {
    type: string;
    data: unknown;
  };
  error?: string;
}

export interface TranscribeResponse {
  success: boolean;
  text: string;
  error?: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: string;
  updatedAt: string;
}

class MathMentorAPI {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  /**
   * Solve a math problem
   */
  async solve(request: SolveRequest): Promise<SolveResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/solve`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Solve API error:", error);
      return {
        success: false,
        solution: "",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Transcribe audio to text
   */
  async transcribe(audioBlob: Blob): Promise<TranscribeResponse> {
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      const response = await fetch(`${this.baseUrl}/api/transcribe`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Transcribe API error:", error);
      return {
        success: false,
        text: "",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Process an image with OCR
   */
  async processImage(imageBase64: string): Promise<{ success: boolean; text: string; error?: string }> {
    try {
      const response = await fetch(`${this.baseUrl}/api/ocr`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: imageBase64 }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("OCR API error:", error);
      return {
        success: false,
        text: "",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  /**
   * Stream a solution (Server-Sent Events)
   */
  streamSolution(
    request: SolveRequest,
    onChunk: (chunk: string) => void,
    onComplete: () => void,
    onError: (error: string) => void
  ): () => void {
    const controller = new AbortController();

    fetch(`${this.baseUrl}/api/solve/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    })
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error("No response body");
        }

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          onChunk(chunk);
        }

        onComplete();
      })
      .catch((error) => {
        if (error.name !== "AbortError") {
          onError(error.message);
        }
      });

    return () => controller.abort();
  }

  /**
   * Get chat history
   */
  async getHistory(): Promise<ChatSession[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/history`);
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("History API error:", error);
      return [];
    }
  }

  /**
   * Get a specific chat session
   */
  async getSession(sessionId: string): Promise<ChatSession | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/sessions/${sessionId}`);
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Session API error:", error);
      return null;
    }
  }
}

// Export singleton instance
export const api = new MathMentorAPI();
export default api;
