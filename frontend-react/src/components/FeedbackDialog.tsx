import { useState } from "react";

export default function FeedbackDialog({
  problem,
  wrongAnswer,
  onSubmit,
  onCancel,
}: {
  problem: string;
  wrongAnswer: string;
  onSubmit: (correctAnswer: string, explanation: string) => void;
  onCancel: () => void;
}) {
  const [correctAnswer, setCorrectAnswer] = useState("");
  const [explanation, setExplanation] = useState("");

  const handleSubmit = () => {
    if (!correctAnswer.trim()) {
      alert("Please provide a correct answer.");
      return;
    }
    onSubmit(correctAnswer, explanation);
  };

  return (
    <div className="absolute inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm p-3 md:p-4 overflow-y-auto">
      <div className="bg-background border border-border/50 rounded-2xl p-4 md:p-6 shadow-2xl max-w-2xl w-full my-auto flex flex-col gap-3 md:gap-4">
        <div>
          <h2 className="text-lg md:text-xl font-semibold text-foreground flex items-center gap-2">
            📝 Provide Correct Answer
          </h2>
          <p className="text-xs md:text-sm text-muted-foreground mt-1 mb-3 md:mb-4">
            Help the AI learn from its mistake. This will be stored in memory.
          </p>
        </div>

        <div className="flex flex-col gap-1.5 md:gap-2">
          <label className="text-xs md:text-sm font-medium text-foreground">
            Original Problem
          </label>
          <textarea
            className="w-full bg-secondary/20 border border-border/50 rounded-xl p-2 md:p-3 text-foreground font-mono text-xs md:text-sm resize-none focus:outline-none"
            value={problem}
            disabled
            rows={2}
          />
        </div>

        <div className="flex flex-col gap-1.5 md:gap-2">
          <label className="text-xs md:text-sm font-medium text-foreground">
            Wrong Answer
          </label>
          <textarea
            className="w-full bg-secondary/20 border border-border/50 rounded-xl p-2 md:p-3 text-foreground font-mono text-xs md:text-sm resize-none focus:outline-none"
            value={wrongAnswer}
            disabled
            rows={2}
          />
        </div>

        <div className="flex flex-col gap-1.5 md:gap-2">
          <label className="text-xs md:text-sm font-medium text-foreground">
            Correct Answer
          </label>
          <input
            type="text"
            className="w-full bg-transparent border border-border/50 rounded-xl p-2 md:p-3 text-foreground text-sm md:text-base focus:outline-none focus:ring-1 focus:ring-primary/50"
            placeholder="e.g., 5.2 or x = 2"
            value={correctAnswer}
            onChange={(e) => setCorrectAnswer(e.target.value)}
          />
        </div>

        <div className="flex flex-col gap-1.5 md:gap-2">
          <label className="text-xs md:text-sm font-medium text-foreground">
            Explanation / Key Lesson
          </label>
          <textarea
            className="w-full bg-transparent border border-border/50 rounded-xl p-2 md:p-3 text-foreground resize-none focus:outline-none focus:ring-1 focus:ring-primary/50 text-xs md:text-sm"
            placeholder="Why is it wrong? e.g., 'You forgot to integrate the constant term'"
            value={explanation}
            onChange={(e) => setExplanation(e.target.value)}
            rows={2}
          />
        </div>

        <div className="flex justify-end gap-2 md:gap-3 mt-3 md:mt-4">
          <button
            onClick={onCancel}
            className="px-3 md:px-4 py-2 rounded-xl hover:bg-secondary/50 text-foreground transition-colors text-xs md:text-sm font-medium touch-manipulation"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="px-3 md:px-4 py-2 rounded-xl bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity text-xs md:text-sm flex items-center gap-2 shadow-[0_0_15px_rgba(52,211,153,0.3)] touch-manipulation"
          >
            Submit Feedback & Re-solve
          </button>
        </div>
      </div>
    </div>
  );
}
