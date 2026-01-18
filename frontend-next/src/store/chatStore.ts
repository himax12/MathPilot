import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  attachments?: {
    type: "image" | "file";
    url: string;
    name: string;
  }[];
  isStreaming?: boolean;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

export type Mode = "solve" | "explain" | "practice" | "graph";

interface ChatStore {
  // Current chat state
  messages: Message[];
  isLoading: boolean;
  currentSessionId: string | null;
  currentMode: Mode;
  
  // UI state
  sidebarCollapsed: boolean;
  showAudioRecorder: boolean;
  showImageUpload: boolean;
  
  // Chat history
  sessions: ChatSession[];
  
  // Actions
  addMessage: (message: Omit<Message, "id" | "timestamp">) => void;
  updateMessage: (id: string, content: string) => void;
  setLoading: (loading: boolean) => void;
  setMode: (mode: Mode) => void;
  clearChat: () => void;
  
  // Session management
  createSession: (title: string) => string;
  loadSession: (sessionId: string) => void;
  deleteSession: (sessionId: string) => void;
  
  // UI actions
  toggleSidebar: () => void;
  setShowAudioRecorder: (show: boolean) => void;
  setShowImageUpload: (show: boolean) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Initial state
      messages: [],
      isLoading: false,
      currentSessionId: null,
      currentMode: "solve",
      sidebarCollapsed: false,
      showAudioRecorder: false,
      showImageUpload: false,
      sessions: [],

      // Add a new message
      addMessage: (message) => {
        const newMessage: Message = {
          ...message,
          id: Date.now().toString(),
          timestamp: new Date(),
        };

        set((state) => ({
          messages: [...state.messages, newMessage],
        }));

        // Update session if exists
        const { currentSessionId, sessions } = get();
        if (currentSessionId) {
          const updatedSessions = sessions.map((s) =>
            s.id === currentSessionId
              ? { ...s, messages: [...s.messages, newMessage], updatedAt: new Date() }
              : s
          );
          set({ sessions: updatedSessions });
        }
      },

      // Update an existing message (for streaming)
      updateMessage: (id, content) => {
        set((state) => ({
          messages: state.messages.map((m) =>
            m.id === id ? { ...m, content, isStreaming: false } : m
          ),
        }));
      },

      // Set loading state
      setLoading: (loading) => set({ isLoading: loading }),

      // Set current mode
      setMode: (mode) => set({ currentMode: mode }),

      // Clear current chat
      clearChat: () => {
        const sessionId = Date.now().toString();
        set({
          messages: [],
          currentSessionId: sessionId,
        });
      },

      // Create a new session
      createSession: (title) => {
        const sessionId = Date.now().toString();
        const newSession: ChatSession = {
          id: sessionId,
          title,
          messages: [],
          createdAt: new Date(),
          updatedAt: new Date(),
        };

        set((state) => ({
          sessions: [newSession, ...state.sessions.slice(0, 19)], // Keep last 20 sessions
          currentSessionId: sessionId,
          messages: [],
        }));

        return sessionId;
      },

      // Load an existing session
      loadSession: (sessionId) => {
        const { sessions } = get();
        const session = sessions.find((s) => s.id === sessionId);
        if (session) {
          set({
            currentSessionId: sessionId,
            messages: session.messages,
          });
        }
      },

      // Delete a session
      deleteSession: (sessionId) => {
        set((state) => ({
          sessions: state.sessions.filter((s) => s.id !== sessionId),
          currentSessionId:
            state.currentSessionId === sessionId ? null : state.currentSessionId,
          messages: state.currentSessionId === sessionId ? [] : state.messages,
        }));
      },

      // Toggle sidebar
      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      // UI state setters
      setShowAudioRecorder: (show) => set({ showAudioRecorder: show }),
      setShowImageUpload: (show) => set({ showImageUpload: show }),
    }),
    {
      name: "math-mentor-chat",
      partialize: (state) => ({
        sessions: state.sessions,
        sidebarCollapsed: state.sidebarCollapsed,
      }),
    }
  )
);

export default useChatStore;
