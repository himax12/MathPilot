import { MessageSquarePlus, MessageSquare, Menu } from "lucide-react";
import { useState } from "react";
import { cn } from "../lib/utils";
import { ThemeToggle } from "./ThemeToggle";

export default function Sidebar({
  sessions,
  currentSessionId,
  onNewChat,
  onSelectSession,
}: {
  sessions: any[];
  currentSessionId: string | null;
  onNewChat: () => void;
  onSelectSession: (id: string) => void;
}) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div
      className={cn(
        "flex flex-col bg-card/20 backdrop-blur-2xl border-r border-border/30 transition-all duration-300 z-20",
        isOpen ? "w-[280px]" : "w-[72px]"
      )}
    >
      <div className="flex items-center justify-between p-6 h-20 border-b border-white/5">
        {isOpen && (
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-medium tracking-tighter text-foreground">
              MathPilot<span className="text-primary">.</span>
            </h2>
          </div>
        )}
        <div className="flex items-center gap-1">
          {isOpen && <ThemeToggle />}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-1.5 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground transition-colors"
          >
            <Menu size={20} />
          </button>
        </div>
      </div>

      <div className="p-4 mt-2">
        <button
          onClick={onNewChat}
          className="flex items-center justify-center gap-2 w-full p-2.5 rounded-full border border-white/10 text-muted-foreground hover:text-foreground hover:border-white/20 hover:bg-white/5 transition-all group font-light text-sm"
        >
          <MessageSquarePlus size={16} strokeWidth={1.5} />
          {isOpen && <span>New Thread</span>}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-2 scrollbar-thin">
        {isOpen && (
          <div className="text-[10px] font-mono text-muted-foreground/50 py-3 uppercase tracking-widest pl-2">
            History
          </div>
        )}
        <div className="space-y-0.5 mt-1">
          {sessions.map((s) => (
            <button
              key={s.session_id}
              onClick={() => onSelectSession(s.session_id)}
              className={cn(
                "flex items-center gap-3 w-full px-2 py-2.5 rounded-lg text-sm text-left transition-all duration-300",
                currentSessionId === s.session_id
                  ? "text-foreground font-medium bg-white/5"
                  : "text-muted-foreground/70 hover:text-foreground hover:bg-white/5"
              )}
            >
              <MessageSquare size={14} strokeWidth={currentSessionId === s.session_id ? 2 : 1.5} className={currentSessionId === s.session_id ? "text-primary" : "shrink-0"} />
              {isOpen && (
                <span className="truncate font-light tracking-wide">
                  {s.title || `Session ${s.session_id.substring(0, 6)}`}
                </span>
              )}
            </button>
          ))}
          {sessions.length === 0 && isOpen && (
             <div className="px-2 py-4 text-xs font-light text-muted-foreground/50 italic opacity-70">No history yet.</div>
          )}
        </div>
      </div>
      
      {isOpen && (
         <div className="p-4 border-t border-white/5">
            <div className="p-3 text-center">
               <div className="text-xs text-muted-foreground font-light mb-0.5">Powered by</div>
               <div className="font-semibold text-sm text-foreground tracking-tight mb-3">Agentic RAG</div>
               <button className="text-[11px] font-medium tracking-widest uppercase text-muted-foreground hover:text-primary transition-colors flex items-center justify-center gap-1 mx-auto group">
                  Upgrade to Pro <span className="group-hover:translate-x-1 transition-transform">→</span>
               </button>
            </div>
         </div>
      )}
    </div>
  );
}
