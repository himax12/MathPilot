"use client";

import { useState, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import MicIcon from "@mui/icons-material/Mic";
import StopIcon from "@mui/icons-material/Stop";
import CloseIcon from "@mui/icons-material/Close";

interface AudioRecorderProps {
  onTranscription: (text: string) => void;
  onClose: () => void;
}

/**
 * AudioRecorder: Voice input with waveform visualization
 * 
 * Uses Web Speech API for browser-native recognition
 * Falls back to backend transcription if needed
 */
export default function AudioRecorder({ onTranscription, onClose }: AudioRecorderProps) {
  const [status, setStatus] = useState<"idle" | "recording" | "processing">("idle");
  const [duration, setDuration] = useState(0);
  const [transcript, setTranscript] = useState("");
  
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const startRecording = useCallback(() => {
    // Check for Web Speech API support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      setTranscript(finalTranscript || interimTranscript);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      stopRecording();
    };

    recognition.onend = () => {
      if (status === "recording") {
        setStatus("processing");
      }
    };

    recognitionRef.current = recognition;
    recognition.start();
    setStatus("recording");
    setDuration(0);

    // Start timer
    timerRef.current = setInterval(() => {
      setDuration((prev) => prev + 1);
    }, 1000);
  }, [status]);

  const stopRecording = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setStatus("processing");

    // Small delay to ensure final transcript is captured
    setTimeout(() => {
      if (transcript.trim()) {
        onTranscription(transcript);
      }
      setStatus("idle");
      onClose();
    }, 500);
  }, [transcript, onTranscription, onClose]);

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="absolute bottom-20 left-4 right-4 bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 shadow-xl"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white font-medium">Voice Input</h3>
        <button
          onClick={onClose}
          className="p-1 text-gray-400 hover:text-white rounded hover:bg-[#2a2a2a]"
        >
          <CloseIcon style={{ fontSize: 18 }} />
        </button>
      </div>

      {/* Waveform Visualization */}
      <div className="flex items-center justify-center h-16 mb-4">
        {status === "recording" && (
          <div className="flex items-center gap-1">
            {[...Array(12)].map((_, i) => (
              <motion.div
                key={i}
                animate={{
                  height: [8, Math.random() * 40 + 8, 8],
                }}
                transition={{
                  duration: 0.5,
                  repeat: Infinity,
                  delay: i * 0.05,
                }}
                className="w-1 bg-[#4ADE80] rounded-full"
              />
            ))}
          </div>
        )}
        {status === "processing" && (
          <div className="flex items-center gap-2 text-gray-400">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full"
            />
            <span>Processing...</span>
          </div>
        )}
        {status === "idle" && !transcript && (
          <p className="text-gray-400 text-sm">Click the microphone to start recording</p>
        )}
      </div>

      {/* Transcript Preview */}
      {transcript && (
        <div className="bg-[#0a0a0a] rounded-lg p-3 mb-4 max-h-20 overflow-y-auto">
          <p className="text-gray-300 text-sm">{transcript}</p>
        </div>
      )}

      {/* Controls */}
      <div className="flex items-center justify-center gap-4">
        {status === "idle" && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={startRecording}
            className="w-14 h-14 rounded-full bg-[#4ADE80] text-black flex items-center justify-center hover:bg-[#22C55E] transition-colors"
          >
            <MicIcon style={{ fontSize: 28 }} />
          </motion.button>
        )}
        {status === "recording" && (
          <>
            <span className="text-white font-mono">{formatDuration(duration)}</span>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={stopRecording}
              className="w-14 h-14 rounded-full bg-red-500 text-white flex items-center justify-center hover:bg-red-600 transition-colors"
            >
              <StopIcon style={{ fontSize: 28 }} />
            </motion.button>
            <motion.div
              animate={{ opacity: [1, 0.5, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="w-3 h-3 rounded-full bg-red-500"
            />
          </>
        )}
      </div>
    </motion.div>
  );
}

// TypeScript declarations for Web Speech API
declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition;
    webkitSpeechRecognition: typeof SpeechRecognition;
  }
}
