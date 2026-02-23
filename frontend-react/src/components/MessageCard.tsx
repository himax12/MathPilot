import { Copy, RotateCw, Check, X, Edit2 } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

export default function MessageCard({
  msg,
  isActive,
  onFeedbackPositive,
  onFeedbackNegative,
  onEditSubmit,
}: {
  msg: any;
  isActive?: boolean;
  onFeedbackPositive?: () => void;
  onFeedbackNegative?: () => void;
  onEditSubmit?: (newContent: string) => void;
}) {
  const isUser = msg.role === "user";
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(msg.content);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (isEditing && textareaRef.current) {
      textareaRef.current.style.height = "inherit";
      textareaRef.current.style.height = `${Math.max(textareaRef.current.scrollHeight, 60)}px`;
      textareaRef.current.focus();
      textareaRef.current.setSelectionRange(
        textareaRef.current.value.length,
        textareaRef.current.value.length,
      );
    }
  }, [isEditing]);

  const handleCopy = () => {
    navigator.clipboard.writeText(msg.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleEditSave = () => {
    if (editValue.trim() !== "" && onEditSubmit) {
      onEditSubmit(editValue);
    }
    setIsEditing(false);
  };

  const handleEditCancel = () => {
    setEditValue(msg.content);
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleEditSave();
    } else if (e.key === "Escape") {
      handleEditCancel();
    }
  };

  return (
    <div
      className={`flex w-full group mb-4 md:mb-6 ${isUser ? "justify-end" : "justify-start"}`}
    >
      <div
        className={`flex gap-3 md:gap-4 w-full md:max-w-[85%] lg:max-w-[75%] ${isUser ? "flex-row-reverse max-w-[95%] md:max-w-[85%]" : "max-w-full flex-row"}`}
      >
        {/* Minimalist Avatar Replacement */}
        {!isUser && (
          <div className="shrink-0 pt-1">
            <div className="w-7 h-7 md:w-8 md:h-8 rounded-lg md:rounded-xl flex items-center justify-center bg-primary/10 border border-primary/20 text-primary font-bold text-xs md:text-sm shadow-[0_0_15px_rgba(52,211,153,0.15)] backdrop-blur-sm">
              M
            </div>
          </div>
        )}

        {/* Message Bubble container - flexible width for editing */}
        <div
          className={`flex flex-col gap-1 min-w-0 ${isEditing ? "w-full" : ""}`}
        >
          {/* Sender Name */}
          <span
            className={`text-[10px] md:text-[11px] font-medium tracking-wide uppercase px-1 ${isUser ? "text-muted-foreground/50 text-right" : "text-primary/70 text-left"}`}
          >
            {isUser ? "You" : "MathPilot"}
          </span>

          {/* Content Box */}
          <div
            className={`relative px-4 py-3 md:px-5 md:py-4 transition-all duration-300 ${
              isUser
                ? "bg-white/5 border border-white/10 rounded-xl md:rounded-2xl rounded-tr-sm text-foreground/90 backdrop-blur-sm"
                : isActive
                  ? "bg-primary/[0.03] border border-primary/20 rounded-xl md:rounded-2xl rounded-tl-sm shadow-[0_0_30px_rgba(52,211,153,0.05)] text-foreground/95 backdrop-blur-sm"
                  : "bg-transparent border border-transparent hover:border-white/5 rounded-xl md:rounded-2xl rounded-tl-sm text-foreground/90"
            } ${isEditing ? "w-full ring-1 ring-primary/50" : ""}`}
          >
            {msg.imageUrl && (
              <div className="mb-2 md:mb-3 flex items-center gap-2 md:gap-3 bg-black/20 p-2 rounded-lg md:rounded-xl border border-white/5 w-fit">
                <img
                  src={msg.imageUrl}
                  alt="Uploaded"
                  className="h-8 md:h-10 w-auto rounded-md object-contain"
                />
              </div>
            )}

            {isEditing ? (
              <div className="flex flex-col gap-2 md:gap-3">
                <textarea
                  ref={textareaRef}
                  value={editValue}
                  onChange={(e) => {
                    setEditValue(e.target.value);
                    e.target.style.height = "inherit";
                    e.target.style.height = `${e.target.scrollHeight}px`;
                  }}
                  onKeyDown={handleKeyDown}
                  className="w-full bg-black/20 border border-white/10 rounded-lg md:rounded-xl p-2 md:p-3 text-sm md:text-base text-foreground/90 resize-none focus:outline-none focus:border-primary/50 min-h-[60px]"
                  placeholder="Edit your message..."
                />
                <div className="flex justify-end gap-2">
                  <button
                    onClick={handleEditCancel}
                    className="px-3 py-1.5 text-xs font-medium bg-white/5 hover:bg-white/10 text-muted-foreground rounded-lg transition-colors flex items-center gap-1.5 touch-manipulation"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleEditSave}
                    disabled={editValue.trim() === ""}
                    className="px-3 py-1.5 text-xs font-medium bg-primary/20 hover:bg-primary/30 text-primary border border-primary/30 rounded-lg transition-colors flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed touch-manipulation"
                  >
                    Save & Submit
                  </button>
                </div>
              </div>
            ) : (
              <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none break-words font-light leading-relaxed prose-p:leading-relaxed prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-xl whitespace-pre-wrap">
                <ReactMarkdown
                  remarkPlugins={[remarkMath, remarkGfm]}
                  rehypePlugins={[rehypeKatex]}
                  components={{
                    code({ node, inline, className, children, ...props }: any) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline && match ? (
                        <div className="relative group/code mt-4 mb-4 rounded-xl overflow-hidden bg-[#050505] border border-white/5">
                          <div className="flex items-center justify-between px-4 py-2 bg-white/[0.02] border-b border-white/5">
                            <span className="text-[10px] text-muted-foreground/50 font-mono uppercase tracking-widest">
                              {match[1]}
                            </span>
                            <button
                              onClick={() =>
                                navigator.clipboard.writeText(
                                  String(children).replace(/\n$/, ""),
                                )
                              }
                              className="text-muted-foreground/40 hover:text-foreground opacity-0 group-hover/code:opacity-100 transition-opacity"
                            >
                              <Copy size={13} />
                            </button>
                          </div>
                          <code
                            className="block p-4 overflow-x-auto text-[13px] font-mono text-emerald-300"
                            {...props}
                          >
                            {children}
                          </code>
                        </div>
                      ) : (
                        <code
                          className="bg-white/5 px-1.5 py-0.5 rounded text-emerald-400 font-mono text-[13px]"
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {msg.content}
                </ReactMarkdown>
              </div>
            )}

            {/* Action Buttons */}
            {!isEditing && (
              <div
                className={`absolute -bottom-3 md:-bottom-4 ${isUser ? "left-1 md:left-2" : "right-1 md:right-2"} flex items-center gap-0.5 md:gap-1 opacity-100 md:opacity-0 md:group-hover:opacity-100 transition-opacity bg-background/80 backdrop-blur-md rounded-lg p-0.5 md:p-1 border border-white/10 shadow-lg`}
              >
                {isUser ? (
                  <button
                    onClick={() => setIsEditing(true)}
                    className="p-1.5 md:p-1.5 rounded-md text-muted-foreground/50 hover:text-foreground hover:bg-white/5 transition-colors touch-manipulation"
                    title="Edit message"
                  >
                    <Edit2 size={14} className="md:w-[13px] md:h-[13px]" />
                  </button>
                ) : (
                  <>
                    <button
                      onClick={handleCopy}
                      className="p-1.5 md:p-1.5 rounded-md text-muted-foreground/50 hover:text-foreground hover:bg-white/5 transition-colors touch-manipulation"
                      title="Copy message"
                    >
                      {copied ? (
                        <Check
                          size={14}
                          className="text-emerald-400 md:w-[13px] md:h-[13px]"
                        />
                      ) : (
                        <Copy size={14} className="md:w-[13px] md:h-[13px]" />
                      )}
                    </button>
                    <button
                      className="p-1.5 md:p-1.5 rounded-md text-muted-foreground/50 hover:text-foreground hover:bg-white/5 transition-colors touch-manipulation"
                      title="Regenerate response"
                    >
                      <RotateCw size={14} className="md:w-[13px] md:h-[13px]" />
                    </button>
                    <button
                      onClick={onFeedbackPositive}
                      className="p-1.5 md:p-1.5 rounded-md text-muted-foreground/50 hover:text-emerald-400 hover:bg-white/5 transition-colors touch-manipulation"
                      title="Correct response"
                    >
                      <Check size={14} className="md:w-[13px] md:h-[13px]" />
                    </button>
                    <button
                      onClick={onFeedbackNegative}
                      className="p-1.5 md:p-1.5 rounded-md text-muted-foreground/50 hover:text-destructive hover:bg-white/5 transition-colors touch-manipulation"
                      title="Incorrect response"
                    >
                      <X size={14} className="md:w-[13px] md:h-[13px]" />
                    </button>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
