"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import AddIcon from "@mui/icons-material/Add";
import ExploreIcon from "@mui/icons-material/Explore";
import CategoryIcon from "@mui/icons-material/Category";
import FolderIcon from "@mui/icons-material/Folder";
import SettingsIcon from "@mui/icons-material/Settings";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import MenuIcon from "@mui/icons-material/Menu";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";

interface ChatSession {
  id: string;
  title: string;
  preview: string;
  timestamp: Date;
}

interface SidebarProps {
  isCollapsed?: boolean;
  onToggle?: () => void;
  onNewChat?: () => void;
}

/**
 * Sidebar Component - Responsive
 * 
 * Purpose: Navigation, chat history, and user profile
 * Width: 220px desktop, collapsible on mobile
 */
export default function Sidebar({ isCollapsed = false, onToggle, onNewChat }: SidebarProps) {
  const [activeNav, setActiveNav] = useState<string>("explore");
  const [chatHistory, setChatHistory] = useState<ChatSession[]>([
    { id: "1", title: "Solve quadratic equation", preview: "x² + 5x + 6 = 0", timestamp: new Date() },
    { id: "2", title: "Integration help", preview: "∫ sin(x) dx", timestamp: new Date() },
    { id: "3", title: "Matrix multiplication", preview: "3x3 matrix problem", timestamp: new Date() },
  ]);
  const [hoveredChat, setHoveredChat] = useState<string | null>(null);

  const navItems = [
    { id: "explore", icon: ExploreIcon, label: "Explore" },
    { id: "categories", icon: CategoryIcon, label: "Categories" },
    { id: "library", icon: FolderIcon, label: "Library", badge: chatHistory.length },
    { id: "settings", icon: SettingsIcon, label: "Settings" },
  ];

  const deleteChat = (id: string) => {
    setChatHistory((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <>
      {/* Mobile Overlay */}
      <AnimatePresence>
        {!isCollapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onToggle}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{
          width: isCollapsed ? 0 : 220,
          x: isCollapsed ? -220 : 0,
        }}
        transition={{ duration: 0.2, ease: "easeInOut" }}
        className={`h-full bg-[#141414] border-r border-[#2a2a2a] flex flex-col overflow-hidden
          fixed lg:relative z-50 lg:z-auto`}
      >
        {/* Logo */}
        <div className="h-14 flex items-center justify-between px-4 border-b border-[#2a2a2a] shrink-0">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center">
              <span className="text-white text-lg font-bold">π</span>
            </div>
            <span className="text-white font-semibold whitespace-nowrap">Math Mentor</span>
          </div>
          <button
            onClick={onToggle}
            className="p-1 text-gray-400 hover:text-white rounded hover:bg-[#2a2a2a] lg:hidden"
          >
            <ChevronLeftIcon style={{ fontSize: 20 }} />
          </button>
        </div>

        {/* New Chat Button */}
        <div className="p-3 shrink-0">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onNewChat}
            className="w-full h-10 bg-[#4ADE80] hover:bg-[#22C55E] text-black font-medium rounded-lg flex items-center justify-center gap-2 transition-colors"
          >
            <AddIcon fontSize="small" />
            New Chat
          </motion.button>
        </div>

        {/* Navigation */}
        <nav className="px-2 space-y-1 shrink-0">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveNav(item.id)}
              className={`w-full h-10 px-3 rounded-lg flex items-center gap-3 transition-colors ${
                activeNav === item.id
                  ? "bg-[#2a2a2a] text-white"
                  : "text-gray-400 hover:bg-[#1a1a1a] hover:text-white"
              }`}
            >
              <item.icon fontSize="small" />
              <span className="text-sm whitespace-nowrap">{item.label}</span>
              {item.badge && (
                <span className="ml-auto text-xs bg-[#2a2a2a] text-gray-400 px-2 py-0.5 rounded">
                  {item.badge}
                </span>
              )}
            </button>
          ))}
        </nav>

        {/* Divider */}
        <div className="my-3 mx-3 border-t border-[#2a2a2a]" />

        {/* Chat History Label */}
        <div className="px-4 py-2">
          <span className="text-xs text-gray-500 uppercase tracking-wide">Chats</span>
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto px-2 space-y-1">
          {chatHistory.map((chat) => (
            <motion.div
              key={chat.id}
              onMouseEnter={() => setHoveredChat(chat.id)}
              onMouseLeave={() => setHoveredChat(null)}
              className="relative"
            >
              <button
                className="w-full px-3 py-2 rounded-lg text-left hover:bg-[#1a1a1a] transition-colors group"
              >
                <div className="flex items-start gap-2">
                  <ChatBubbleOutlineIcon className="text-gray-500 mt-0.5 shrink-0" style={{ fontSize: 16 }} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-300 truncate">{chat.title}</p>
                    <p className="text-xs text-gray-500 truncate">{chat.preview}</p>
                  </div>
                </div>
              </button>
              {/* Delete button on hover */}
              <AnimatePresence>
                {hoveredChat === chat.id && (
                  <motion.button
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.8 }}
                    onClick={() => deleteChat(chat.id)}
                    className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-gray-500 hover:text-red-400 rounded hover:bg-[#2a2a2a]"
                  >
                    <DeleteOutlineIcon style={{ fontSize: 16 }} />
                  </motion.button>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>

        {/* User Profile */}
        <div className="p-3 border-t border-[#2a2a2a] shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shrink-0">
              <span className="text-white text-sm font-medium">U</span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white truncate">User</p>
            </div>
            <button className="p-1.5 text-gray-400 hover:text-white rounded hover:bg-[#2a2a2a]">
              <NotificationsNoneIcon fontSize="small" />
            </button>
            <button className="p-1.5 text-gray-400 hover:text-white rounded hover:bg-[#2a2a2a]">
              <DarkModeIcon fontSize="small" />
            </button>
          </div>
        </div>
      </motion.aside>

      {/* Mobile Menu Button (when collapsed) */}
      {isCollapsed && (
        <button
          onClick={onToggle}
          className="fixed top-4 left-4 z-50 p-2 bg-[#1a1a1a] rounded-lg text-gray-400 hover:text-white lg:hidden"
        >
          <MenuIcon />
        </button>
      )}
    </>
  );
}
