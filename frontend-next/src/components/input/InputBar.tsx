"use client";

import { useState, useRef, KeyboardEvent } from "react";
import { motion, AnimatePresence } from "framer-motion";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import MicIcon from "@mui/icons-material/Mic";
import SendIcon from "@mui/icons-material/Send";
import FunctionsIcon from "@mui/icons-material/Functions";
import SchoolIcon from "@mui/icons-material/School";
import EditNoteIcon from "@mui/icons-material/EditNote";
import TimelineIcon from "@mui/icons-material/Timeline";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import CloseIcon from "@mui/icons-material/Close";
import AudioRecorder from "./AudioRecorder";
import ImageUpload from "./ImageUpload";

interface InputBarProps {
  onSendMessage: (content: string, mode: string, image?: { file: File; preview: string }) => void;
  isLoading: boolean;
}

type Mode = "solve" | "explain" | "practice" | "graph";

/**
 * InputBar: Multi-modal input with mode switching
 * 
 * Supports text, audio, and file attachments
 * Mode tabs: Solve, Explain, Practice, Graph
 */
export default function InputBar({ onSendMessage, isLoading }: InputBarProps) {
  const [text, setText] = useState("");
  const [mode, setMode] = useState<Mode>("solve");
  const [showAudioRecorder, setShowAudioRecorder] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [attachedImage, setAttachedImage] = useState<{ file: File; preview: string } | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const modes = [
    { id: "solve" as Mode, icon: FunctionsIcon, label: "Solve", color: "text-green-400" },
    { id: "explain" as Mode, icon: SchoolIcon, label: "Explain", color: "text-blue-400" },
    { id: "practice" as Mode, icon: EditNoteIcon, label: "Practice", color: "text-yellow-400" },
    { id: "graph" as Mode, icon: TimelineIcon, label: "Graph", color: "text-purple-400" },
  ];

  const handleSubmit = () => {
    if ((text.trim() || attachedImage) && !isLoading) {
      onSendMessage(text, mode, attachedImage || undefined);
      setText("");
      setAttachedImage(null);
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    
    // Auto-expand textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const handleTranscription = (transcribedText: string) => {
    setText((prev) => (prev ? `${prev} ${transcribedText}` : transcribedText));
    setShowAudioRecorder(false);
  };

  const handleImageSelect = (file: File, preview: string) => {
    setAttachedImage({ file, preview });
    setShowImageUpload(false);
  };

  return (
    <div className="shrink-0 border-t border-[#2a2a2a] p-4 relative">
      {/* Audio Recorder Overlay */}
      <AnimatePresence>
        {showAudioRecorder && (
          <AudioRecorder
            onTranscription={handleTranscription}
            onClose={() => setShowAudioRecorder(false)}
          />
        )}
      </AnimatePresence>

      {/* Image Upload Overlay */}
      <AnimatePresence>
        {showImageUpload && (
          <ImageUpload
            onImageSelect={handleImageSelect}
            onClose={() => setShowImageUpload(false)}
          />
        )}
      </AnimatePresence>

      {/* Mode Selector */}
      <div className="flex items-center gap-2 mb-3">
        {modes.map((m) => (
          <motion.button
            key={m.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setMode(m.id)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm transition-all ${
              mode === m.id
                ? `bg-[#2a2a2a] ${m.color} border border-[#3a3a3a]`
                : "text-gray-400 hover:text-white hover:bg-[#1a1a1a]"
            }`}
          >
            <m.icon style={{ fontSize: 16 }} />
            {m.label}
          </motion.button>
        ))}
        <button className="p-1.5 text-gray-500 hover:text-white">
          <MoreHorizIcon style={{ fontSize: 18 }} />
        </button>
      </div>

      {/* Attached Image Preview */}
      <AnimatePresence>
        {attachedImage && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mb-3"
          >
            <div className="relative inline-block">
              <img
                src={attachedImage.preview}
                alt="Attached"
                className="h-20 rounded-lg border border-[#2a2a2a]"
              />
              <button
                onClick={() => setAttachedImage(null)}
                className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center text-white hover:bg-red-600 transition-colors"
              >
                <CloseIcon style={{ fontSize: 14 }} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input Container */}
      <div className="relative bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl focus-within:border-[#4a4a4a] transition-colors">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder={attachedImage ? "Add a message about this image..." : "Ask anything..."}
          disabled={isLoading}
          rows={1}
          className="w-full bg-transparent px-4 py-3 pr-28 text-white placeholder-gray-500 resize-none focus:outline-none min-h-[48px] max-h-[200px]"
        />

        {/* Right Actions */}
        <div className="absolute right-2 bottom-2 flex items-center gap-1">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowImageUpload(true)}
            className={`p-2 rounded-lg transition-colors ${
              attachedImage
                ? "text-[#4ADE80] bg-[#4ADE80]/10"
                : "text-gray-400 hover:text-white hover:bg-[#2a2a2a]"
            }`}
            title="Attach image"
          >
            <AttachFileIcon style={{ fontSize: 20 }} />
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowAudioRecorder(true)}
            className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-[#2a2a2a] transition-colors"
            title="Voice input"
          >
            <MicIcon style={{ fontSize: 20 }} />
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSubmit}
            disabled={(!text.trim() && !attachedImage) || isLoading}
            className={`p-2 rounded-lg transition-all ${
              (text.trim() || attachedImage) && !isLoading
                ? "bg-[#4ADE80] text-black hover:bg-[#22C55E]"
                : "bg-[#2a2a2a] text-gray-500 cursor-not-allowed"
            }`}
            title="Send message"
          >
            <SendIcon style={{ fontSize: 20 }} />
          </motion.button>
        </div>
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-gray-500 text-center mt-2">
        Math Mentor may produce inaccurate results. Always verify important calculations.
      </p>
    </div>
  );
}
