"use client";

import { motion } from "framer-motion";
import BookmarkBorderIcon from "@mui/icons-material/BookmarkBorder";
import CardGiftcardIcon from "@mui/icons-material/CardGiftcard";
import ShuffleIcon from "@mui/icons-material/Shuffle";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import ChatOutlinedIcon from "@mui/icons-material/ChatOutlined";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";

/**
 * UtilityBar Component
 * 
 * Purpose: Quick action icons on right edge
 * Width: 60px
 */
export default function UtilityBar() {
  const utilityItems = [
    { icon: BookmarkBorderIcon, label: "Bookmark", onClick: () => console.log("Bookmark") },
    { icon: CardGiftcardIcon, label: "Rewards", onClick: () => console.log("Rewards") },
    { icon: ShuffleIcon, label: "Random", onClick: () => console.log("Random problem") },
    { icon: InfoOutlinedIcon, label: "Info", onClick: () => console.log("Info") },
    { icon: ChatOutlinedIcon, label: "Feedback", onClick: () => console.log("Feedback") },
    { icon: HelpOutlineIcon, label: "Help", onClick: () => console.log("Help") },
  ];

  return (
    <aside className="w-[60px] h-full bg-transparent border-l border-[#2a2a2a] flex flex-col items-center py-4 gap-2">
      {utilityItems.map((item, index) => (
        <motion.button
          key={index}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={item.onClick}
          className="w-10 h-10 rounded-lg flex items-center justify-center text-gray-500 hover:text-white hover:bg-[#1a1a1a] transition-colors"
          title={item.label}
        >
          <item.icon fontSize="small" />
        </motion.button>
      ))}
    </aside>
  );
}
