"use client";

import { useState } from "react";
import Sidebar from "./Sidebar";
import UtilityBar from "./UtilityBar";

interface MainLayoutProps {
  children: React.ReactNode;
}

/**
 * MainLayout: Root container orchestrating the responsive three-column layout
 * 
 * ┌─────────────────────────────────────────────────────────────┐
 * │ [Sidebar]  │        [children]           │ [UtilityBar]    │
 * │   220px    │         flex-1              │      60px       │
 * └─────────────────────────────────────────────────────────────┘
 * 
 * On mobile: Sidebar is collapsible, UtilityBar hidden
 */
export default function MainLayout({ children }: MainLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(true);

  const handleNewChat = () => {
    // This will be connected to global state
    window.location.reload(); // Simple refresh for now
  };

  return (
    <div className="flex h-screen bg-[#0a0a0a] overflow-hidden">
      {/* Left Sidebar - Responsive */}
      <Sidebar 
        isCollapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
        onNewChat={handleNewChat}
      />
      
      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden min-w-0">
        {children}
      </main>
      
      {/* Right Utility Bar - Hidden on mobile */}
      <div className="hidden md:block">
        <UtilityBar />
      </div>
    </div>
  );
}
