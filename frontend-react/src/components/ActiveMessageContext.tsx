import { createContext, useContext, useState } from "react";

type ActiveMessageContextType = {
  activeMessageIndex: number | null;
  setActiveMessageIndex: (index: number | null) => void;
};

const ActiveMessageContext = createContext<ActiveMessageContextType | undefined>(
  undefined
);

export function ActiveMessageProvider({ children }: { children: React.ReactNode }) {
  const [activeMessageIndex, setActiveMessageIndex] = useState<number | null>(null);

  return (
    <ActiveMessageContext.Provider value={{ activeMessageIndex, setActiveMessageIndex }}>
      {children}
    </ActiveMessageContext.Provider>
  );
}

export function useActiveMessage() {
  const context = useContext(ActiveMessageContext);
  if (context === undefined) {
    throw new Error("useActiveMessage must be used within an ActiveMessageProvider");
  }
  return context;
}
