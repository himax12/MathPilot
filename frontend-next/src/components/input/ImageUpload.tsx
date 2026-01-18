"use client";

import { useState, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import PhotoCameraIcon from "@mui/icons-material/PhotoCamera";
import CloseIcon from "@mui/icons-material/Close";
import ImageIcon from "@mui/icons-material/Image";

interface ImageUploadProps {
  onImageSelect: (file: File, preview: string) => void;
  onClose: () => void;
}

/**
 * ImageUpload: Drag-and-drop image upload with camera option
 * 
 * Supports drag-drop, file picker, and camera capture
 * Shows preview before sending
 */
export default function ImageUpload({ onImageSelect, onClose }: ImageUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) {
      alert("Please select an image file");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
      setSelectedFile(file);
    };
    reader.readAsDataURL(file);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const file = e.dataTransfer.files[0];
      if (file) {
        handleFile(file);
      }
    },
    [handleFile]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        handleFile(file);
      }
    },
    [handleFile]
  );

  const handleConfirm = useCallback(() => {
    if (selectedFile && preview) {
      onImageSelect(selectedFile, preview);
      onClose();
    }
  }, [selectedFile, preview, onImageSelect, onClose]);

  const handleClear = useCallback(() => {
    setPreview(null);
    setSelectedFile(null);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="absolute bottom-20 left-4 right-4 bg-[#1a1a1a] border border-[#2a2a2a] rounded-xl p-4 shadow-xl"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white font-medium">Upload Image</h3>
        <button
          onClick={onClose}
          className="p-1 text-gray-400 hover:text-white rounded hover:bg-[#2a2a2a]"
        >
          <CloseIcon style={{ fontSize: 18 }} />
        </button>
      </div>

      {/* Hidden inputs */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />
      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFileChange}
        className="hidden"
      />

      <AnimatePresence mode="wait">
        {!preview ? (
          // Drop Zone
          <motion.div
            key="dropzone"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
              isDragging
                ? "border-[#4ADE80] bg-[#4ADE80]/10"
                : "border-[#3a3a3a] hover:border-[#4a4a4a]"
            }`}
          >
            <ImageIcon className="mx-auto text-gray-500 mb-3" style={{ fontSize: 48 }} />
            <p className="text-gray-400 mb-4">
              Drag and drop an image here, or
            </p>
            <div className="flex justify-center gap-3">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => fileInputRef.current?.click()}
                className="px-4 py-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-white rounded-lg flex items-center gap-2 transition-colors"
              >
                <CloudUploadIcon style={{ fontSize: 18 }} />
                Browse
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => cameraInputRef.current?.click()}
                className="px-4 py-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-white rounded-lg flex items-center gap-2 transition-colors"
              >
                <PhotoCameraIcon style={{ fontSize: 18 }} />
                Camera
              </motion.button>
            </div>
          </motion.div>
        ) : (
          // Preview
          <motion.div
            key="preview"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-4"
          >
            <div className="relative rounded-xl overflow-hidden bg-[#0a0a0a]">
              <img
                src={preview}
                alt="Preview"
                className="w-full max-h-64 object-contain mx-auto"
              />
              <button
                onClick={handleClear}
                className="absolute top-2 right-2 p-1.5 bg-black/50 hover:bg-black/70 rounded-full text-white transition-colors"
              >
                <CloseIcon style={{ fontSize: 18 }} />
              </button>
            </div>
            <p className="text-gray-400 text-sm text-center">
              {selectedFile?.name} ({(selectedFile?.size || 0 / 1024).toFixed(1)} KB)
            </p>
            <div className="flex justify-center gap-3">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleClear}
                className="px-4 py-2 bg-[#2a2a2a] hover:bg-[#3a3a3a] text-white rounded-lg transition-colors"
              >
                Choose Different
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleConfirm}
                className="px-4 py-2 bg-[#4ADE80] hover:bg-[#22C55E] text-black font-medium rounded-lg transition-colors"
              >
                Use This Image
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
