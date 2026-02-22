import { Copy, ThumbsUp, ThumbsDown, RotateCw, Check } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import remarkGfm from "remark-gfm";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

export default function MessageCard({ msg, isActive }: { msg: any; isActive?: boolean }) {
  const isUser = msg.role === "user";
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(msg.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex w-full group mb-6 ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex gap-4 max-w-[85%] md:max-w-[75%] ${isUser ? "flex-row-reverse" : "flex-row"}`}>
        
        {/* Minimalist Avatar Replacement */}
        {!isUser && (
           <div className="shrink-0 pt-1">
              <div className="w-8 h-8 rounded-xl flex items-center justify-center bg-primary/10 border border-primary/20 text-primary font-bold text-sm shadow-[0_0_15px_rgba(52,211,153,0.15)] backdrop-blur-sm">
                M
              </div>
           </div>
        )}

        {/* Message Bubble */}
        <div className="flex flex-col gap-1 min-w-0">
           {/* Sender Name */}
           <span className={`text-[11px] font-medium tracking-wide uppercase px-1 ${isUser ? "text-muted-foreground/50 text-right" : "text-primary/70 text-left"}`}>
             {isUser ? "You" : "MathPilot"}
           </span>

           {/* Content Box */}
           <div
             className={`relative px-5 py-4 transition-all duration-300 ${
               isUser
                 ? "bg-white/5 border border-white/10 rounded-2xl rounded-tr-sm text-foreground/90 backdrop-blur-sm" 
                 : isActive
                 ? "bg-primary/[0.03] border border-primary/20 rounded-2xl rounded-tl-sm shadow-[0_0_30px_rgba(52,211,153,0.05)] text-foreground/95 backdrop-blur-sm"
                 : "bg-transparent border border-transparent hover:border-white/5 rounded-2xl rounded-tl-sm text-foreground/90"
             }`}
           >
             {msg.imageUrl && (
               <div className="mb-3 flex items-center gap-3 bg-black/20 p-2 rounded-xl border border-white/5 w-fit">
                 <img src={msg.imageUrl} alt="Uploaded" className="h-10 w-auto rounded-md object-contain" />
               </div>
             )}
             <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none break-words font-light leading-relaxed prose-p:leading-relaxed prose-pre:bg-white/5 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-xl">
               <ReactMarkdown
                 remarkPlugins={[remarkMath, remarkGfm]}
                 rehypePlugins={[rehypeKatex]}
                 components={{
                   code({ node, inline, className, children, ...props }: any) {
                     const match = /language-(\w+)/.exec(className || "");
                     return !inline && match ? (
                       <div className="relative group/code mt-4 mb-4 rounded-xl overflow-hidden bg-[#050505] border border-white/5">
                         <div className="flex items-center justify-between px-4 py-2 bg-white/[0.02] border-b border-white/5">
                           <span className="text-[10px] text-muted-foreground/50 font-mono uppercase tracking-widest">{match[1]}</span>
                           <button
                             onClick={() => navigator.clipboard.writeText(String(children).replace(/\n$/, ""))}
                             className="text-muted-foreground/40 hover:text-foreground opacity-0 group-hover/code:opacity-100 transition-opacity"
                           >
                             <Copy size={13} />
                           </button>
                         </div>
                         <code className="block p-4 overflow-x-auto text-[13px] font-mono text-emerald-300" {...props}>
                           {children}
                         </code>
                       </div>
                     ) : (
                       <code className="bg-white/5 px-1.5 py-0.5 rounded text-emerald-400 font-mono text-[13px]" {...props}>
                         {children}
                       </code>
                     );
                   },
                 }}
               >
                 {msg.content}
               </ReactMarkdown>
             </div>

             {/* Action Buttons */}
             {!isUser && (
               <div className="absolute -bottom-4 right-2 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-background/80 backdrop-blur-md rounded-lg p-1 border border-white/10 shadow-lg">
                 <button 
                   onClick={handleCopy}
                   className="p-1.5 rounded-md text-muted-foreground/50 hover:text-foreground hover:bg-white/5 transition-colors"
                   title="Copy message"
                 >
                   {copied ? <Check size={13} className="text-emerald-400" /> : <Copy size={13} />}
                 </button>
                 <button 
                   className="p-1.5 rounded-md text-muted-foreground/50 hover:text-foreground hover:bg-white/5 transition-colors"
                    title="Regenerate response"
                 >
                   <RotateCw size={13} />
                 </button>
                 <button 
                    className="p-1.5 rounded-md text-muted-foreground/50 hover:text-emerald-400 hover:bg-white/5 transition-colors"
                    title="Good response"
                 >
                   <ThumbsUp size={13} />
                 </button>
                 <button 
                    className="p-1.5 rounded-md text-muted-foreground/50 hover:text-destructive hover:bg-white/5 transition-colors"
                    title="Bad response"
                 >
                   <ThumbsDown size={13} />
                 </button>
               </div>
             )}
           </div>
        </div>
      </div>
    </div>
  );
}
