import {
  X,
  AlignRight,
  Component,
  Maximize2,
  Terminal,
  CheckCircle2,
  AlertTriangle,
  BrainCircuit,
  GraduationCap,
  ArrowRight,
} from "lucide-react";
import { useState } from "react";

export default function InspectorPane({
  message,
  onClose,
}: {
  message: any;
  onClose: () => void;
}) {
  const [isDeckExpanded, setIsDeckExpanded] = useState(false);

  if (!message) return null;

  return (
    <>
      <div className="fixed md:relative inset-0 md:inset-auto w-full md:w-[350px] shrink-0 border-l border-white/5 bg-black/40 backdrop-blur-2xl flex flex-col h-full right-pane-animation shadow-2xl z-50 md:z-20 transition-all">
        {/* Header */}
        <div className="flex items-center justify-between p-4 md:p-5 border-b border-white/5 h-14 md:h-16 shrink-0 bg-transparent">
          <h3 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest flex items-center gap-2">
            <AlignRight size={14} /> Context Inspector
          </h3>
          <button
            onClick={onClose}
            className="p-1.5 rounded text-muted-foreground/50 hover:bg-white/5 hover:text-foreground transition-all"
          >
            <X size={18} strokeWidth={1.5} />
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-4 scrollbar-thin">
          {/* Placeholder for tabs. Will be fleshed out in Phase 4 */}
          <div className="space-y-6">
            {/* Deck Preview */}
            {message.deck && (
              <div
                onClick={() => {
                  if (message.deck_html) setIsDeckExpanded(true);
                }}
                className={`bg-white/[0.02] rounded-xl p-5 border border-white/5 transition-all group ${message.deck_html ? "hover:bg-white/[0.04] cursor-pointer" : "opacity-70"}`}
              >
                <div className="flex justify-between items-start mb-3">
                  <h4 className="text-[10px] font-semibold uppercase tracking-widest text-muted-foreground/70 flex items-center gap-2">
                    <Component
                      size={12}
                      className={
                        message.deck_html
                          ? "text-emerald-400/70"
                          : "text-muted-foreground"
                      }
                    />{" "}
                    Visual Deck
                  </h4>
                  {message.deck_html && (
                    <Maximize2
                      size={14}
                      className="text-muted-foreground/40 group-hover:text-emerald-400/70 transition-colors"
                    />
                  )}
                </div>
                <div className="text-[13px] text-foreground/70 font-light transition-colors">
                  {message.deck_html
                    ? "Interactive presentation available. Click to expand player."
                    : "Visual presentation is being generated..."}
                </div>
              </div>
            )}

            {/* Explanation Preview */}
            {message.explanation && !message.explanation.error && (
              <div className="bg-emerald-500/5 rounded-xl p-5 border border-emerald-500/10 backdrop-blur-md">
                <h4 className="text-[10px] font-semibold uppercase tracking-widest text-emerald-400 mb-3">
                  JEE Tutor Insight
                </h4>
                <p className="text-[13px] text-foreground/80 font-light leading-relaxed">
                  {message.explanation.intuition}
                </p>
              </div>
            )}

            {/* Trace Preview */}
            {message.events && message.events.length > 0 && (
              <div className="mt-8 mb-4">
                <div className="flex items-center gap-2 mb-6 px-1">
                  <Terminal size={13} className="text-muted-foreground/50" />
                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground/50">
                    Agent Trace Log
                  </h4>
                </div>

                <div className="relative pl-3">
                  {/* Timeline line */}
                  <div className="absolute left-[19px] top-3 bottom-3 w-[1px] bg-gradient-to-b from-white/10 via-white/5 to-transparent" />

                  <div className="space-y-4">
                    {message.events.map((e: string, i: number) => {
                      let icon = ArrowRight;
                      let colorClass = "text-muted-foreground/40";
                      let bgClass = "bg-white/5 border-white/5";
                      let textClass = "text-muted-foreground/60";
                      let text = e.trim();

                      if (e.includes("✅")) {
                        icon = CheckCircle2;
                        colorClass = "text-emerald-400";
                        bgClass =
                          "bg-emerald-400/10 border-emerald-400/20 shadow-[0_0_10px_rgba(52,211,153,0.1)]";
                        textClass = "text-emerald-50/90";
                        text = text.replace("✅", "").trim();
                      } else if (e.includes("⚠️")) {
                        icon = AlertTriangle;
                        colorClass = "text-amber-400";
                        bgClass =
                          "bg-amber-400/10 border-amber-400/20 shadow-[0_0_10px_rgba(251,191,36,0.1)]";
                        textClass = "text-amber-50/90";
                        text = text.replace("⚠️", "").trim();
                      } else if (e.includes("🧠")) {
                        icon = BrainCircuit;
                        colorClass = "text-purple-400";
                        bgClass =
                          "bg-purple-400/10 border-purple-400/20 shadow-[0_0_10px_rgba(192,132,252,0.1)]";
                        textClass = "text-purple-50/90";
                        text = text.replace("🧠", "").trim();
                      } else if (e.includes("🎓")) {
                        icon = GraduationCap;
                        colorClass = "text-blue-400";
                        bgClass =
                          "bg-blue-400/10 border-blue-400/20 shadow-[0_0_10px_rgba(96,165,250,0.1)]";
                        textClass = "text-blue-50/90";
                        text = text.replace("🎓", "").trim();
                      }

                      const Icon = icon;

                      return (
                        <div
                          key={i}
                          className="relative flex items-start gap-4 group"
                        >
                          <div
                            className={`relative shrink-0 w-4 h-4 rounded-full flex items-center justify-center border z-10 mt-0.5 transition-all duration-300 group-hover:scale-110 ${bgClass}`}
                          >
                            <Icon
                              size={8}
                              className={colorClass}
                              strokeWidth={3}
                            />
                          </div>
                          <div className="flex-1 min-w-0 pt-[1.5px]">
                            <p
                              className={`text-[11px] font-mono leading-relaxed truncate transition-colors ${textClass} group-hover:text-foreground/90`}
                            >
                              {text}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {!message.deck &&
              !message.explanation &&
              (!message.events || message.events.length === 0) && (
                <div className="flex flex-col items-center justify-center text-center py-24 px-4 h-full opacity-60">
                  <Component
                    size={32}
                    strokeWidth={1}
                    className="text-muted-foreground/30 mb-4"
                  />
                  <div className="text-[13px] text-foreground font-light mb-1">
                    No Deep Context
                  </div>
                  <div className="text-[11px] text-muted-foreground font-light">
                    This message was generated without relying on RAG, visual
                    decks, or extended reasoning traces.
                  </div>
                </div>
              )}
          </div>
        </div>
      </div>

      {/* Fullscreen Deck Modal Overlay */}
      {isDeckExpanded && message.deck_html && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-8 animate-in fade-in duration-200">
          <div className="relative w-full max-w-6xl h-full max-h-[90vh] bg-[#1a1a2e] rounded-xl border border-white/10 shadow-2xl flex flex-col overflow-hidden">
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-black/20">
              <h3 className="text-sm font-semibold text-emerald-400 uppercase tracking-widest flex items-center gap-2">
                <Component size={16} /> Math Mentor Presentation Player
              </h3>
              <button
                onClick={() => setIsDeckExpanded(false)}
                className="p-2 rounded-md hover:bg-white/10 transition-colors text-muted-foreground hover:text-white"
              >
                <X size={20} />
              </button>
            </div>

            {/* Iframe Container */}
            <div className="flex-1 bg-white">
              <iframe
                srcDoc={message.deck_html}
                className="w-full h-full border-0"
                title="Visual Deck Player"
                sandbox="allow-scripts allow-same-origin"
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
