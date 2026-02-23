import { useState, useRef, useEffect } from "react";
import {
  Send,
  Image as ImageIcon,
  Mic,
  Loader2,
  Square,
  Menu,
} from "lucide-react";
import MessageCard from "./MessageCard";
import { useActiveMessage } from "./ActiveMessageContext";

export default function ChatWindow({
  messages,
  onSendMessage,
  onUploadImage,
  isLoading,
  currentEvent,
  onFeedbackPositive,
  onFeedbackNegative,
  onEditSubmit,
  onVoiceInput,
  onMenuClick,
}: {
  messages: any[];
  onSendMessage: (msg: string) => void;
  onUploadImage: (file: File) => void;
  isLoading: boolean;
  currentEvent?: string | null;
  onFeedbackPositive?: (msgIndex: number) => void;
  onFeedbackNegative?: (msgIndex: number) => void;
  onEditSubmit?: (msgIndex: number, newContent: string) => void;
  onVoiceInput?: (audioBlob: Blob) => void;
  onMenuClick?: () => void;
}) {
  const [input, setInput] = useState("");
  const endRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { activeMessageIndex, setActiveMessageIndex } = useActiveMessage();

  // Audio recording state
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    onSendMessage(input);
    setInput("");
  };

  const handleImageClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUploadImage(file);
      // Reset so the same file can be re-selected
      e.target.value = "";
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/webm",
        });
        if (onVoiceInput) {
          onVoiceInput(audioBlob);
        }
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Failed to start recording", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="flex flex-col h-full relative w-full overflow-hidden bg-background">
      {/* Dynamic Background Glowing Orbs */}
      <div className="glow-orb glow-orb-green w-[600px] h-[600px] -top-32 right-10"></div>
      <div className="glow-orb glow-orb-blue w-[500px] h-[500px] top-64 -left-32"></div>
      <div className="glow-orb glow-orb-purple w-[400px] h-[400px] bottom-10 right-32"></div>

      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between px-4 py-3 border-b border-white/5 bg-card/20 backdrop-blur-2xl z-20">
        <button
          onClick={onMenuClick}
          className="p-2 rounded-lg hover:bg-white/5 text-foreground transition-colors"
        >
          <Menu size={20} />
        </button>
        <h2 className="text-lg font-medium tracking-tighter text-foreground">
          MathPilot<span className="text-primary">.</span>
        </h2>
        <div className="w-9" /> {/* Spacer for centering */}
      </div>

      {/* Hidden file input for image upload */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 md:px-8 lg:px-16 xl:px-32 scrollbar-thin relative z-10">
        {messages.length === 0 && !isLoading ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4 mt-[-10vh]">
            <h1 className="text-4xl md:text-5xl lg:text-7xl font-extralight text-foreground mb-4 md:mb-6 tracking-tighter">
              MathPilot<span className="text-primary font-bold">.</span>
            </h1>
            <p className="text-muted-foreground/80 text-base md:text-lg lg:text-xl max-w-xl mx-auto font-light tracking-wide leading-relaxed">
              An agentic reasoning engine for complex mathematics.
            </p>

            <div className="flex flex-col gap-4 md:gap-6 mt-12 md:mt-16 w-full max-w-2xl justify-center items-stretch md:flex-row md:items-center">
              <button
                className="group flex flex-col items-start text-left hover:opacity-70 transition-opacity p-4 md:p-0 rounded-xl md:rounded-none bg-white/5 md:bg-transparent border border-white/5 md:border-none"
                onClick={() =>
                  setInput("Solve the integral of x^2 * sin(x) dx")
                }
              >
                <div className="font-medium text-foreground text-xs md:text-sm tracking-widest uppercase mb-1 md:mb-2 flex items-center gap-2">
                  <span className="text-primary/70">/</span> Calculus
                </div>
                <div className="text-sm text-muted-foreground font-light">
                  Solve the integral of x^2 * sin(x) dx
                </div>
              </button>

              <div className="hidden md:block w-px h-12 bg-white/5 mx-4"></div>

              <button
                className="group flex flex-col items-start text-left hover:opacity-70 transition-opacity p-4 md:p-0 rounded-xl md:rounded-none bg-white/5 md:bg-transparent border border-white/5 md:border-none"
                onClick={() => setInput("Find the roots of 3x^2 - 12x + 5 = 0")}
              >
                <div className="font-medium text-foreground text-xs md:text-sm tracking-widest uppercase mb-1 md:mb-2 flex items-center gap-2">
                  <span className="text-primary/70">/</span> Algebra
                </div>
                <div className="text-sm text-muted-foreground font-light">
                  Find the roots of 3x^2 - 12x + 5 = 0
                </div>
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-8 md:space-y-12 pb-32 md:pb-36">
            {messages.map((msg, i) => (
              <div
                key={i}
                onClick={() => setActiveMessageIndex(i)}
                className={`cursor-pointer transition-all duration-300 rounded-2xl md:rounded-3xl p-1 md:p-2 ${activeMessageIndex === i ? "bg-primary/5 shadow-[0_0_30px_rgba(52,211,153,0.05)] ring-1 ring-primary/20" : "hover:bg-secondary/30"}`}
              >
                <MessageCard
                  msg={msg}
                  onFeedbackPositive={
                    onFeedbackPositive ? () => onFeedbackPositive(i) : undefined
                  }
                  onFeedbackNegative={
                    onFeedbackNegative ? () => onFeedbackNegative(i) : undefined
                  }
                  onEditSubmit={
                    onEditSubmit
                      ? (newContent) => onEditSubmit(i, newContent)
                      : undefined
                  }
                />
              </div>
            ))}

            {/* Thinking indicator — shown while waiting for API response */}
            {isLoading && (
              <div className="flex gap-3 md:gap-4 max-w-[95%] md:max-w-[85%] lg:max-w-[75%]">
                <div className="shrink-0 pt-1">
                  <div className="w-7 h-7 md:w-8 md:h-8 rounded-xl flex items-center justify-center bg-primary/10 border border-primary/20 text-primary font-bold text-xs md:text-sm shadow-[0_0_15px_rgba(52,211,153,0.15)] backdrop-blur-sm">
                    M
                  </div>
                </div>
                <div className="flex flex-col gap-1 min-w-0">
                  <span className="text-[10px] md:text-[11px] font-medium tracking-wide uppercase px-1 text-primary/70 text-left">
                    MathPilot
                  </span>
                  <div className="flex items-center gap-2 px-4 md:px-5 py-3 md:py-4 text-muted-foreground/60 text-xs md:text-sm font-light">
                    <Loader2
                      size={14}
                      className="animate-spin text-primary/60 shrink-0"
                    />
                    <span className="truncate">
                      {currentEvent || "Thinking…"}
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div ref={endRef} />
          </div>
        )}
      </div>

      {/* Ultra Minimalist Input Area */}
      <div className="absolute bottom-0 left-0 right-0 p-4 md:p-6 bg-gradient-to-t from-background via-background/90 to-transparent z-20">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-2 md:gap-3 pb-2 border-b border-white/10 relative transition-all focus-within:border-primary/50">
            {/* Image upload button */}
            <button
              onClick={handleImageClick}
              disabled={isLoading}
              className="pb-2 text-muted-foreground/50 hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed transition-colors shrink-0 touch-manipulation"
              title="Upload image for OCR"
            >
              <ImageIcon
                size={20}
                strokeWidth={1}
                className="md:w-5 md:h-5 w-6 h-6"
              />
            </button>

            <button
              onClick={toggleRecording}
              disabled={isLoading}
              className={`pb-2 transition-colors shrink-0 touch-manipulation ${isRecording ? "text-destructive scale-110 animate-pulse" : "text-muted-foreground/50 hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed"}`}
              title={isRecording ? "Stop recording" : "Voice input"}
            >
              {isRecording ? (
                <Square
                  size={20}
                  strokeWidth={2}
                  fill="currentColor"
                  className="md:w-5 md:h-5 w-6 h-6"
                />
              ) : (
                <Mic
                  size={20}
                  strokeWidth={1}
                  className="md:w-5 md:h-5 w-6 h-6"
                />
              )}
            </button>

            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder={
                isLoading ? "Waiting for response…" : "Ask anything…"
              }
              disabled={isLoading}
              className="flex-1 bg-transparent border-none focus:outline-none focus:ring-0 resize-none max-h-48 min-h-[30px] p-0 pb-1.5 text-foreground placeholder-muted-foreground/50 disabled:opacity-50 disabled:cursor-not-allowed scrollbar-thin text-base leading-relaxed font-light"
              rows={1}
            />

            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="pb-2 text-primary hover:text-primary/70 disabled:opacity-30 disabled:text-muted-foreground disabled:cursor-not-allowed transition-all shrink-0 touch-manipulation"
            >
              {isLoading ? (
                <Loader2
                  size={20}
                  className="animate-spin md:w-5 md:h-5 w-6 h-6"
                  strokeWidth={1.5}
                />
              ) : (
                <Send
                  size={20}
                  className="translate-x-[1px] md:w-5 md:h-5 w-6 h-6"
                  strokeWidth={1.5}
                />
              )}
            </button>
          </div>
          <div className="text-center mt-2 md:mt-3 mb-1 md:mb-2">
            <span className="text-[10px] md:text-xs text-muted-foreground/60">
              MathPilot AI can make mistakes. Consider checking important math
              steps.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
