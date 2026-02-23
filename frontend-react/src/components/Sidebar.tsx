import {
  MessageSquarePlus,
  MessageSquare,
  Menu,
  Edit3,
  Check,
  X,
  Trash2,
} from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { cn } from "../lib/utils";
import { ThemeToggle } from "./ThemeToggle";
import { useAuth } from "../context/AuthContext";
import { LogOut, User as UserIcon } from "lucide-react";

export default function Sidebar({
  sessions,
  currentSessionId,
  onNewChat,
  onSelectSession,
  onRenameSession,
  onDeleteSession,
  isMobileOpen,
  onMobileClose,
}: {
  sessions: any[];
  currentSessionId: string | null;
  onNewChat: () => void;
  onSelectSession: (id: string) => void;
  onRenameSession: (id: string, newTitle: string) => void;
  onDeleteSession: (id: string) => void;
  isMobileOpen?: boolean;
  onMobileClose?: () => void;
}) {
  const [isOpen, setIsOpen] = useState(true);
  const { user, logout } = useAuth();

  // State for renaming
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editTitleValue, setEditTitleValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input when editing starts
  useEffect(() => {
    if (editingSessionId && inputRef.current) {
      inputRef.current.focus();
    }
  }, [editingSessionId]);

  const handleStartEdit = (
    e: React.MouseEvent,
    id: string,
    currentTitle: string,
  ) => {
    e.stopPropagation();
    setEditingSessionId(id);
    setEditTitleValue(currentTitle);
  };

  const handleSaveEdit = (
    e: React.MouseEvent | React.KeyboardEvent,
    id: string,
  ) => {
    e.stopPropagation();
    if (editTitleValue.trim()) {
      onRenameSession(id, editTitleValue.trim());
    }
    setEditingSessionId(null);
  };

  const handleCancelEdit = (e: React.MouseEvent | React.KeyboardEvent) => {
    e.stopPropagation();
    setEditingSessionId(null);
  };

  const handleDeleteClick = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this session?")) {
      onDeleteSession(id);
    }
  };

  return (
    <>
      {/* Mobile overlay backdrop */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden"
          onClick={onMobileClose}
        />
      )}

      <div
        className={cn(
          "flex flex-col bg-card/20 backdrop-blur-2xl border-r border-border/30 transition-all duration-300 z-50",
          // Mobile: fixed overlay that slides in from left
          "fixed md:relative inset-y-0 left-0",
          "md:z-20",
          // Hide on mobile by default, show when isMobileOpen is true
          isMobileOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0",
          // Desktop: normal behavior
          isOpen ? "w-[280px]" : "w-[72px]",
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
            {sessions.map((s) => {
              const isEditing = editingSessionId === s.session_id;
              const currentTitle =
                s.title || `Session ${s.session_id.substring(0, 6)}`;

              return (
                <div
                  key={s.session_id}
                  onClick={() => {
                    if (!isEditing) {
                      onSelectSession(s.session_id);
                      onMobileClose?.();
                    }
                  }}
                  className={cn(
                    "group relative flex items-center gap-3 w-full px-2 py-2.5 rounded-lg text-sm transition-all duration-300",
                    currentSessionId === s.session_id
                      ? "text-foreground font-medium bg-white/5"
                      : "text-muted-foreground/70 hover:text-foreground hover:bg-white/5",
                    isEditing ? "cursor-default" : "cursor-pointer",
                  )}
                >
                  {!isEditing && (
                    <MessageSquare
                      size={14}
                      strokeWidth={currentSessionId === s.session_id ? 2 : 1.5}
                      className={
                        currentSessionId === s.session_id
                          ? "text-primary"
                          : "shrink-0"
                      }
                    />
                  )}

                  {isOpen && (
                    <>
                      {isEditing ? (
                        <div
                          className="flex items-center w-full gap-1"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <input
                            ref={inputRef}
                            type="text"
                            value={editTitleValue}
                            onChange={(e) => setEditTitleValue(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === "Enter")
                                handleSaveEdit(e, s.session_id);
                              if (e.key === "Escape") handleCancelEdit(e);
                            }}
                            className="flex-1 bg-black/40 border border-white/20 text-foreground text-sm rounded px-2 py-1 focus:outline-none focus:border-primary w-full"
                          />
                          <button
                            onClick={(e) => handleSaveEdit(e, s.session_id)}
                            className="p-1 text-emerald-400 hover:bg-emerald-400/20 rounded"
                          >
                            <Check size={14} />
                          </button>
                          <button
                            onClick={handleCancelEdit}
                            className="p-1 text-red-400 hover:bg-red-400/20 rounded"
                          >
                            <X size={14} />
                          </button>
                        </div>
                      ) : (
                        <>
                          <span className="flex-1 truncate font-light tracking-wide text-left">
                            {currentTitle}
                          </span>

                          <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-0.5 absolute right-2">
                            <button
                              onClick={(e) =>
                                handleStartEdit(e, s.session_id, currentTitle)
                              }
                              className="p-1 hover:bg-white/10 rounded text-muted-foreground hover:text-foreground"
                              title="Rename"
                            >
                              <Edit3 size={12} />
                            </button>
                            <button
                              onClick={(e) =>
                                handleDeleteClick(e, s.session_id)
                              }
                              className="p-1 hover:bg-red-500/10 rounded text-muted-foreground hover:text-red-400"
                              title="Delete"
                            >
                              <Trash2 size={12} />
                            </button>
                          </div>
                        </>
                      )}
                    </>
                  )}
                </div>
              );
            })}
            {sessions.length === 0 && isOpen && (
              <div className="px-2 py-4 text-xs font-light text-muted-foreground/50 italic opacity-70">
                No history yet.
              </div>
            )}
          </div>
        </div>

        {isOpen && (
          <div className="p-4 border-t border-white/5">
            {user && (
              <div className="flex items-center gap-3 mb-4 p-2 rounded-xl bg-white/5 border border-white/5">
                {user.picture ? (
                  <img
                    src={user.picture}
                    alt={user.name}
                    className="w-8 h-8 rounded-full border border-white/10"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center border border-white/10">
                    <UserIcon size={16} className="text-primary" />
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">
                    {user.name}
                  </p>
                  <p className="text-[10px] text-muted-foreground truncate">
                    {user.email}
                  </p>
                </div>
                <button
                  onClick={logout}
                  className="p-1.5 hover:bg-white/10 rounded-lg text-muted-foreground hover:text-red-400 transition-colors"
                  title="Logout"
                >
                  <LogOut size={16} />
                </button>
              </div>
            )}
            <div className="p-3 text-center">
              <div className="text-xs text-muted-foreground font-light mb-0.5">
                Powered by
              </div>
              <div className="font-semibold text-sm text-foreground tracking-tight mb-3">
                Agentic RAG
              </div>
              <button className="text-[11px] font-medium tracking-widest uppercase text-muted-foreground hover:text-primary transition-colors flex items-center justify-center gap-1 mx-auto group">
                Upgrade to Pro{" "}
                <span className="group-hover:translate-x-1 transition-transform">
                  →
                </span>
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
