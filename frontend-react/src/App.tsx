import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import InspectorPane from "./components/InspectorPane";
import {
  ActiveMessageProvider,
  useActiveMessage,
} from "./components/ActiveMessageContext";
import FeedbackDialog from "./components/FeedbackDialog";
import { api } from "./lib/api";
import { useAuth } from "./context/AuthContext";
import Login from "./components/Login";

function MathPilotApp() {
  const [sessions, setSessions] = useState<any[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentEvent, setCurrentEvent] = useState<string | null>(null);
  const [pendingOcr, setPendingOcr] = useState<{
    latex: string;
    problem_data: any;
    imageUrl?: string;
  } | null>(null);
  const [pendingFeedback, setPendingFeedback] = useState<{
    problem: string;
    wrongAnswer: string;
  } | null>(null);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const { isAuthenticated, isLoading: authLoading, logout } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      fetchSessions();
    }
  }, [isAuthenticated]);

  const fetchSessions = async () => {
    try {
      const data = await api.getSessions();
      setSessions(data.sessions ?? []);
    } catch (e: any) {
      console.error("Failed to fetch sessions", e);
      if (e.message?.includes("401")) {
        logout();
      }
    }
  };

  const handleNewChat = async () => {
    try {
      await api.clearSession();
      setCurrentSessionId(null);
      setMessages([]);
      fetchSessions();
    } catch (e) {
      console.error(e);
    }
  };

  const handleSelectSession = async (id: string) => {
    try {
      const data = await api.restoreSession(id);
      if (data.success) {
        setCurrentSessionId(id);
        setMessages(
          (data.messages ?? []).map((m: any) => ({
            ...m,
            deck_html: m.deck_html || null,
          })),
        );
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSendMessage = async (text: string) => {
    // Optimistic user bubble
    const userMsg = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);
    setCurrentEvent("Initializing...");

    try {
      const data = await api.chatStream(text, setCurrentEvent);
      const assistantMsg = {
        role: "assistant",
        content: data.response,
        deck: data.deck,
        deck_html: data.deck_html,
        explanation: data.explanation,
        events: data.events,
        confidence: data.confidence,
        status: data.status,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      fetchSessions();
    } catch (e: any) {
      setError(e?.message ?? "Failed to reach backend. Is the server running?");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Could not get a response. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadImage = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const ocr: any = await api.uploadImage(file);
      if (ocr.success && ocr.latex) {
        const imageUrl = await new Promise<string>((resolve) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result as string);
          reader.readAsDataURL(file);
        });
        setPendingOcr({
          latex: ocr.latex,
          problem_data: ocr.problem_data,
          imageUrl,
        });
      } else {
        setError(
          ocr.error ||
            "OCR failed. Please try a clearer image or ensure it contains math.",
        );
      }
    } catch (e: any) {
      setError(e?.message ?? "Image upload failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceInput = async (audioBlob: Blob) => {
    setIsLoading(true);
    setError(null);
    setCurrentEvent("Transcribing voice...");
    try {
      const file = new File([audioBlob], "recording.webm", {
        type: "audio/webm",
      });
      const res = await api.transcribeAudio(file);
      if (res.success && res.text) {
        handleSendMessage(res.text);
      } else {
        setError(
          res.error || "Could not transcribe audio. Speak more clearly?",
        );
      }
    } catch (e: any) {
      setError(e?.message ?? "Voice transcription failed.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleConfirmOcr = async (ocrData: {
    latex: string;
    problem_data: any;
    imageUrl?: string;
  }) => {
    setPendingOcr(null);

    // Convert \( \) to $ $ and \[ \] to $$ $$ so that remarkMath correctly detects it.
    let cleanLatex = ocrData.latex
      .replace(/\\\(/g, "$")
      .replace(/\\\)/g, "$")
      .replace(/\\\[/g, "$$$$")
      .replace(/\\\]/g, "$$$$")
      .trim();

    const userMsg = {
      role: "user",
      content: cleanLatex,
      imageUrl: ocrData.imageUrl,
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);
    setCurrentEvent("Initialzing...");

    try {
      const data = await api.chatStream(
        { latex: ocrData.latex, problem_data: ocrData.problem_data },
        setCurrentEvent,
      );
      const assistantMsg = {
        role: "assistant",
        content: data.response,
        deck: data.deck,
        deck_html: data.deck_html,
        explanation: data.explanation,
        events: data.events,
        confidence: data.confidence,
        status: data.status,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      fetchSessions();
    } catch (e: any) {
      setError(e?.message ?? "Failed to reach backend during reasoning.");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Could not get a response. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedbackPositive = async (msgIndex: number) => {
    // We could make an API call to log positive feedback if needed.
    // For now, simple toast / alert representation
    console.log("Positive feedback registered for msg", msgIndex);
    // You could use a toast library here, relying on console or alert as a basic visual indicator.
  };

  const handleFeedbackNegative = (msgIndex: number) => {
    const msg = messages[msgIndex];
    if (!msg || msg.role !== "assistant") return;

    // Find the closest preceding user message as the "problem"
    let problemText = "Unknown Problem";
    for (let i = msgIndex - 1; i >= 0; i--) {
      if (messages[i].role === "user") {
        problemText = messages[i].content;
        break;
      }
    }

    // Try to extract a clean wrong answer from explanation/solution state if structured, otherwise fallback to message content
    let wrongAns = "See above";
    // Usually the answer is part of the final text or structured explanation
    if (msg.explanation && msg.explanation.answer) {
      wrongAns = msg.explanation.answer;
    } else if (msg.content) {
      // If content is short, use it, else truncate
      wrongAns = msg.content.length < 100 ? msg.content : "See above";
    }

    setPendingFeedback({ problem: problemText, wrongAnswer: wrongAns });
  };

  const handleSubmitFeedback = async (
    correctAnswer: string,
    explanation: string,
  ) => {
    if (!pendingFeedback) return;
    const { problem, wrongAnswer } = pendingFeedback;
    setPendingFeedback(null);

    setIsLoading(true);
    setCurrentEvent("Submitting feedback...");

    try {
      await api.submitFeedback({
        problem,
        wrong_answer: wrongAnswer,
        correct_answer: correctAnswer,
        explanation,
      });

      // Implicitly send a retry message after feedback
      const retryText = `Please re-solve this problem: ${problem}\n\nNote: Your previous answer (${wrongAnswer}) was incorrect. The correct answer is ${correctAnswer}. Keep this lesson in mind: ${explanation}`;
      await handleSendMessage(retryText);
    } catch (e: any) {
      setError(e?.message ?? "Failed to submit feedback.");
      setIsLoading(false);
    }
  };

  const handleEditSubmit = async (msgIndex: number, newContent: string) => {
    // Keep messages only up to (but not including) the edited message
    // and then send the new content as a new message.
    const newMessages = messages.slice(0, msgIndex);
    setMessages(newMessages);
    await handleSendMessage(newContent);
  };

  const handleRenameSession = async (id: string, newTitle: string) => {
    try {
      await api.updateSessionTitle(id, newTitle);
      await fetchSessions();
    } catch (e: any) {
      setError(e?.message ?? "Failed to rename session.");
    }
  };

  const handleDeleteSession = async (id: string) => {
    try {
      await api.deleteSession(id);
      await fetchSessions();
      if (currentSessionId === id) {
        handleNewChat();
      }
    } catch (e: any) {
      setError(e?.message ?? "Failed to delete session.");
    }
  };

  const { activeMessageIndex, setActiveMessageIndex } = useActiveMessage();

  if (authLoading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-background">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans">
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onNewChat={handleNewChat}
        onSelectSession={handleSelectSession}
        onRenameSession={handleRenameSession}
        onDeleteSession={handleDeleteSession}
        isMobileOpen={isMobileSidebarOpen}
        onMobileClose={() => setIsMobileSidebarOpen(false)}
      />

      {/* Middle Column: Main Chat */}
      <main className="flex-1 flex flex-col relative h-full max-w-full overflow-hidden border-r border-border/20">
        {/* Error Banner */}
        {error && (
          <div className="absolute top-2 md:top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2 md:gap-3 bg-destructive/10 border border-destructive/30 text-destructive text-xs md:text-sm px-3 md:px-4 py-2 md:py-2.5 rounded-xl backdrop-blur-sm shadow-lg max-w-[calc(100%-2rem)] md:max-w-xl w-full mx-auto">
            <span className="flex-1">{error}</span>
            <button
              onClick={() => setError(null)}
              className="shrink-0 opacity-60 hover:opacity-100 transition-opacity text-lg leading-none touch-manipulation"
            >
              ×
            </button>
          </div>
        )}
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          onUploadImage={handleUploadImage}
          isLoading={isLoading}
          currentEvent={currentEvent}
          onFeedbackPositive={handleFeedbackPositive}
          onFeedbackNegative={handleFeedbackNegative}
          onEditSubmit={handleEditSubmit}
          onVoiceInput={handleVoiceInput}
          onMenuClick={() => setIsMobileSidebarOpen(true)}
        />
      </main>

      {/* Right Column: Context Inspector */}
      {activeMessageIndex !== null && messages[activeMessageIndex] && (
        <InspectorPane
          message={messages[activeMessageIndex]}
          onClose={() => setActiveMessageIndex(null)}
        />
      )}

      {/* OCR Verification Modal */}
      {pendingOcr && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-3 md:p-4 overflow-y-auto">
          <div className="bg-background border border-border/50 rounded-2xl p-4 md:p-6 shadow-2xl max-w-4xl w-full my-auto">
            <h2 className="text-lg md:text-xl font-semibold mb-3 md:mb-4 text-foreground">
              Verify Math Extraction
            </h2>
            <p className="text-xs md:text-sm text-muted-foreground mb-3 md:mb-4">
              Please check if the text below matches your image. Mathematical
              notation is written in LaTeX. You can edit the text if there are
              any errors.
            </p>
            <div className="flex flex-col gap-3 md:gap-4 mb-3 md:mb-4">
              {pendingOcr.imageUrl && (
                <div className="flex-1 bg-secondary/10 border border-border/30 rounded-xl overflow-hidden flex justify-center items-center min-h-[150px] md:min-h-[200px]">
                  <img
                    src={pendingOcr.imageUrl}
                    alt="Uploaded math problem"
                    className="max-w-full max-h-[250px] md:max-h-[400px] object-contain"
                  />
                </div>
              )}
              <div className="flex-1 flex flex-col">
                <textarea
                  className="w-full flex-1 min-h-[120px] md:min-h-[200px] bg-secondary/20 border border-border/50 rounded-xl p-3 md:p-4 text-foreground font-mono text-xs md:text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none"
                  value={pendingOcr.latex}
                  onChange={(e) =>
                    setPendingOcr({ ...pendingOcr, latex: e.target.value })
                  }
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 md:gap-3 mt-4 md:mt-6">
              <button
                onClick={() => setPendingOcr(null)}
                className="px-4 md:px-5 py-2 rounded-xl hover:bg-secondary/50 text-foreground transition-colors text-sm md:text-base touch-manipulation"
              >
                Cancel
              </button>
              <button
                onClick={() => handleConfirmOcr(pendingOcr)}
                className="px-4 md:px-5 py-2 rounded-xl bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity flex items-center gap-2 text-sm md:text-base touch-manipulation"
              >
                Solve Problem
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Feedback Modal */}
      {pendingFeedback && (
        <FeedbackDialog
          problem={pendingFeedback.problem}
          wrongAnswer={pendingFeedback.wrongAnswer}
          onSubmit={handleSubmitFeedback}
          onCancel={() => setPendingFeedback(null)}
        />
      )}
    </div>
  );
}

function App() {
  return (
    <ActiveMessageProvider>
      <MathPilotApp />
    </ActiveMessageProvider>
  );
}

export default App;
