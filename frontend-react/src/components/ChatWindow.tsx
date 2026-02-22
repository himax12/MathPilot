import { useState, useRef, useEffect } from "react";
import { Send, Image as ImageIcon, Mic, Loader2 } from "lucide-react";
import MessageCard from "./MessageCard";
import { useActiveMessage } from "./ActiveMessageContext";

export default function ChatWindow({
  messages,
  onSendMessage,
  onUploadImage,
  isLoading,
}: {
  messages: any[];
  onSendMessage: (msg: string) => void;
  onUploadImage: (file: File) => void;
  isLoading: boolean;
}) {
  const [input, setInput] = useState("");
  const endRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { activeMessageIndex, setActiveMessageIndex } = useActiveMessage();

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

  return (
    <div className="flex flex-col h-full relative w-full overflow-hidden bg-background">
      {/* Dynamic Background Glowing Orbs */}
      <div className="glow-orb glow-orb-green w-[600px] h-[600px] -top-32 right-10"></div>
      <div className="glow-orb glow-orb-blue w-[500px] h-[500px] top-64 -left-32"></div>
      <div className="glow-orb glow-orb-purple w-[400px] h-[400px] bottom-10 right-32"></div>

      {/* Hidden file input for image upload */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-8 md:px-16 lg:px-48 scrollbar-thin relative z-10">
        {messages.length === 0 && !isLoading ? (
          <div className="flex flex-col items-center justify-center h-full text-center mt-[-10vh]">
            <h1 className="text-5xl md:text-7xl font-extralight text-foreground mb-6 tracking-tighter">
              MathPilot<span className="text-primary font-bold">.</span>
            </h1>
            <p className="text-muted-foreground/80 text-lg md:text-xl max-w-xl mx-auto font-light tracking-wide leading-relaxed">
              An agentic reasoning engine for complex mathematics.
            </p>

            <div className="flex flex-col md:flex-row gap-6 mt-16 w-full max-w-2xl justify-center items-center">
               <button
                  className="group flex flex-col items-center md:items-start text-left hover:opacity-70 transition-opacity"
                  onClick={() => setInput("Solve the integral of x^2 * sin(x) dx")}
               >
                  <div className="font-medium text-foreground text-sm tracking-widest uppercase mb-2 flex items-center gap-2">
                     <span className="text-primary/70">/</span> Calculus
                  </div>
                  <div className="text-sm text-muted-foreground font-light">Solve the integral of x^2 * sin(x) dx</div>
               </button>

               <div className="hidden md:block w-px h-12 bg-white/5 mx-4"></div>

               <button
                  className="group flex flex-col items-center md:items-start text-left hover:opacity-70 transition-opacity"
                  onClick={() => setInput("Find the roots of 3x^2 - 12x + 5 = 0")}
               >
                  <div className="font-medium text-foreground text-sm tracking-widest uppercase mb-2 flex items-center gap-2">
                     <span className="text-primary/70">/</span> Algebra
                  </div>
                  <div className="text-sm text-muted-foreground font-light">Find the roots of 3x^2 - 12x + 5 = 0</div>
               </button>
            </div>
          </div>
        ) : (
          <div className="space-y-12 pb-32">
            {messages.map((msg, i) => (
              <div
                key={i}
                onClick={() => setActiveMessageIndex(i)}
                className={`cursor-pointer transition-all duration-300 rounded-3xl p-2 ${activeMessageIndex === i ? 'bg-primary/5 shadow-[0_0_30px_rgba(52,211,153,0.05)] ring-1 ring-primary/20' : 'hover:bg-secondary/30'}`}
              >
                <MessageCard msg={msg} />
              </div>
            ))}

            {/* Thinking indicator — shown while waiting for API response */}
            {isLoading && (
              <div className="flex gap-4 max-w-[85%] md:max-w-[75%]">
                <div className="shrink-0 pt-1">
                  <div className="w-8 h-8 rounded-xl flex items-center justify-center bg-primary/10 border border-primary/20 text-primary font-bold text-sm shadow-[0_0_15px_rgba(52,211,153,0.15)] backdrop-blur-sm">
                    M
                  </div>
                </div>
                <div className="flex flex-col gap-1 min-w-0">
                  <span className="text-[11px] font-medium tracking-wide uppercase px-1 text-primary/70 text-left">MathPilot</span>
                  <div className="flex items-center gap-2 px-5 py-4 text-muted-foreground/60 text-sm font-light">
                    <Loader2 size={14} className="animate-spin text-primary/60 shrink-0" />
                    <span>Thinking…</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={endRef} />
          </div>
        )}
      </div>

      {/* Ultra Minimalist Input Area */}
      <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-background via-background/90 to-transparent z-20">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-3 pb-2 border-b border-white/10 relative transition-all focus-within:border-primary/50">

            {/* Image upload button */}
            <button
              onClick={handleImageClick}
              disabled={isLoading}
              className="pb-2 text-muted-foreground/50 hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed transition-colors shrink-0"
              title="Upload image for OCR"
            >
              <ImageIcon size={20} strokeWidth={1} />
            </button>

            <button
              disabled={isLoading}
              className="pb-2 text-muted-foreground/50 hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed transition-colors shrink-0"
              title="Voice input (coming soon)"
            >
              <Mic size={20} strokeWidth={1} />
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
              placeholder={isLoading ? "Waiting for response…" : "Ask anything…"}
              disabled={isLoading}
              className="flex-1 bg-transparent border-none focus:outline-none focus:ring-0 resize-none max-h-48 min-h-[30px] p-0 pb-1.5 text-foreground placeholder-muted-foreground/50 disabled:opacity-50 disabled:cursor-not-allowed scrollbar-thin text-[16px] leading-relaxed font-light"
              rows={1}
            />

            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="pb-2 text-primary hover:text-primary/70 disabled:opacity-30 disabled:text-muted-foreground disabled:cursor-not-allowed transition-all shrink-0"
            >
              {isLoading
                ? <Loader2 size={20} className="animate-spin" strokeWidth={1.5} />
                : <Send size={20} className="translate-x-[1px]" strokeWidth={1.5} />
              }
            </button>
          </div>
          <div className="text-center mt-3 mb-2">
             <span className="text-xs text-muted-foreground/60">MathPilot AI can make mistakes. Consider checking important math steps.</span>
          </div>
        </div>
      </div>
    </div>
  );
}
