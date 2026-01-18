"use client";

interface MessageBubbleProps {
  content: string;
  timestamp: Date;
  avatar?: string;
  attachments?: {
    type: "image" | "file";
    url: string;
    name: string;
  }[];
}

/**
 * MessageBubble: User message display
 * 
 * Right-aligned with user avatar
 * Supports image attachments
 */
export default function MessageBubble({ content, timestamp, attachments }: MessageBubbleProps) {
  return (
    <div className="flex justify-end gap-3">
      <div className="max-w-[70%]">
        {/* Image Attachments */}
        {attachments && attachments.length > 0 && (
          <div className="mb-2 flex flex-wrap gap-2 justify-end">
            {attachments.map((attachment, index) => (
              attachment.type === "image" && (
                <img
                  key={index}
                  src={attachment.url}
                  alt={attachment.name}
                  className="max-h-48 rounded-xl border border-[#2a2a2a]"
                />
              )
            ))}
          </div>
        )}

        {/* Text Content */}
        {content && (
          <div className="bg-[#3a3a3a] rounded-2xl rounded-br-md px-4 py-3">
            <p className="text-white whitespace-pre-wrap">{content}</p>
          </div>
        )}

        {/* Timestamp */}
        <p className="text-xs text-gray-500 text-right mt-1">
          {timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </p>
      </div>

      {/* Avatar */}
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shrink-0">
        <span className="text-white text-sm font-medium">U</span>
      </div>
    </div>
  );
}
