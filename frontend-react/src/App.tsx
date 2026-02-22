import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import ChatWindow from './components/ChatWindow'
import InspectorPane from './components/InspectorPane'
import { ActiveMessageProvider, useActiveMessage } from './components/ActiveMessageContext'
import { api } from './lib/api'

function MathPilotApp() {
  const [sessions, setSessions] = useState<any[]>([])
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pendingOcr, setPendingOcr] = useState<{ latex: string, problem_data: any, imageUrl?: string } | null>(null)

  useEffect(() => {
    fetchSessions()
  }, [])

  const fetchSessions = async () => {
    try {
      const data = await api.getSessions()
      setSessions(data.sessions ?? [])
    } catch (e) {
      console.error("Failed to fetch sessions", e)
    }
  }

  const handleNewChat = async () => {
    try {
      await api.clearSession()
      setCurrentSessionId(null)
      setMessages([])
      fetchSessions()
    } catch (e) {
      console.error(e)
    }
  }

  const handleSelectSession = async (id: string) => {
    try {
      const data = await api.restoreSession(id)
      if (data.success) {
        setCurrentSessionId(id)
        setMessages((data.messages ?? []).map((m: any) => ({
          ...m,
          deck_html: m.deck_html || null
        })))
      }
    } catch (e) {
      console.error(e)
    }
  }

  const handleSendMessage = async (text: string) => {
    // Optimistic user bubble
    const userMsg = { role: "user", content: text }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)
    setError(null)

    try {
      const data = await api.chat(text)
      const assistantMsg = {
        role: "assistant",
        content: data.response,
        deck: data.deck,
        deck_html: data.deck_html,
        explanation: data.explanation,
        events: data.events,
        confidence: data.confidence,
        status: data.status,
      }
      setMessages(prev => [...prev, assistantMsg])
      fetchSessions()
    } catch (e: any) {
      setError(e?.message ?? "Failed to reach backend. Is the server running?")
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Could not get a response. Please try again." }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleUploadImage = async (file: File) => {
    setIsLoading(true)
    setError(null)
    try {
      const ocr: any = await api.uploadImage(file)
      if (ocr.success && ocr.latex) {
        const imageUrl = await new Promise<string>((resolve) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result as string);
          reader.readAsDataURL(file);
        });
        setPendingOcr({ latex: ocr.latex, problem_data: ocr.problem_data, imageUrl })
      } else {
        setError(ocr.error || "OCR failed. Please try a clearer image or ensure it contains math.")
      }
    } catch (e: any) {
      setError(e?.message ?? "Image upload failed.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleConfirmOcr = async (ocrData: { latex: string, problem_data: any, imageUrl?: string }) => {
    setPendingOcr(null)
    const preview = ocrData.latex.replace(/\s+/g, ' ').trim()
    const userMsg = { 
      role: "user", 
      content: `> ${preview.substring(0, 250)}${preview.length > 250 ? '…' : ''}`,
      imageUrl: ocrData.imageUrl
    }
    setMessages(prev => [...prev, userMsg])
    setIsLoading(true)
    setError(null)

    try {
        const data = await api.chat({ latex: ocrData.latex, problem_data: ocrData.problem_data })
        const assistantMsg = {
          role: "assistant",
          content: data.response,
          deck: data.deck,
          deck_html: data.deck_html,
          explanation: data.explanation,
          events: data.events,
          confidence: data.confidence,
          status: data.status,
        }
        setMessages(prev => [...prev, assistantMsg])
        fetchSessions()
    } catch (e: any) {
      setError(e?.message ?? "Failed to reach backend during reasoning.")
      setMessages(prev => [...prev, { role: "assistant", content: "⚠️ Could not get a response. Please try again." }])
    } finally {
      setIsLoading(false)
    }
  }


  const { activeMessageIndex, setActiveMessageIndex } = useActiveMessage()

  return (
    <div className="flex h-screen w-full bg-background text-foreground overflow-hidden font-sans">
      <Sidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onNewChat={handleNewChat}
        onSelectSession={handleSelectSession}
      />

      {/* Middle Column: Main Chat */}
      <main className="flex-1 flex flex-col relative h-full max-w-full overflow-hidden border-r border-border/20">
        {/* Error Banner */}
        {error && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 bg-destructive/10 border border-destructive/30 text-destructive text-sm px-4 py-2.5 rounded-xl backdrop-blur-sm shadow-lg max-w-xl w-full mx-auto">
            <span className="flex-1">{error}</span>
            <button onClick={() => setError(null)} className="shrink-0 opacity-60 hover:opacity-100 transition-opacity text-lg leading-none">×</button>
          </div>
        )}
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          onUploadImage={handleUploadImage}
          isLoading={isLoading}
        />
      </main>

      {/* Right Column: Context Inspector */}
      {activeMessageIndex !== null && messages[activeMessageIndex] && (
        <InspectorPane
          message={messages[activeMessageIndex]}
          onClose={() => setActiveMessageIndex(null)}
        />
      )}

      {/* OCR Verification Modal */}
      {pendingOcr && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto">
          <div className="bg-background border border-border/50 rounded-2xl p-6 shadow-2xl max-w-4xl w-full my-auto">
            <h2 className="text-xl font-semibold mb-4 text-foreground">Verify Math Extraction</h2>
            <p className="text-sm text-muted-foreground mb-4">
              Please check if the text below matches your image. Mathematical notation is written in LaTeX. You can edit the text if there are any errors.
            </p>
            <div className="flex flex-col md:flex-row gap-4 mb-4">
              {pendingOcr.imageUrl && (
                <div className="flex-1 bg-secondary/10 border border-border/30 rounded-xl overflow-hidden flex justify-center items-center min-h-[200px]">
                  <img src={pendingOcr.imageUrl} alt="Uploaded math problem" className="max-w-full max-h-[400px] object-contain" />
                </div>
              )}
              <div className="flex-1 flex flex-col">
                <textarea
                  className="w-full flex-1 min-h-[200px] bg-secondary/20 border border-border/50 rounded-xl p-4 text-foreground font-mono text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none"
                  value={pendingOcr.latex}
                  onChange={(e) => setPendingOcr({...pendingOcr, latex: e.target.value})}
                />
              </div>
            </div>
            <div className="flex justify-end gap-3 mt-6">
              <button 
                onClick={() => setPendingOcr(null)}
                className="px-5 py-2 rounded-xl hover:bg-secondary/50 text-foreground transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleConfirmOcr(pendingOcr)}
                className="px-5 py-2 rounded-xl bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity flex items-center gap-2"
              >
                Solve Problem
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function App() {
  return (
    <ActiveMessageProvider>
      <MathPilotApp />
    </ActiveMessageProvider>
  )
}

export default App
