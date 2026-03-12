import { Bot, MessageSquare, Mic, Terminal } from "lucide-react";
import { motion } from "framer-motion";

interface Props {
  onSuggestion: (text: string) => void;
}

const suggestions = [
  { icon: MessageSquare, text: "Tell me about yourself", color: "text-primary" },
  { icon: Terminal, text: "Show me a code example", color: "text-primary" },
  { icon: Mic, text: "What can you help me with?", color: "text-primary" },
];

export function EmptyState({ onSuggestion }: Props) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="text-center max-w-md"
      >
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6 glow-primary">
          <Bot className="w-9 h-9 text-primary" />
        </div>
        <h2 className="text-2xl font-semibold text-foreground mb-2 tracking-tight">
          How can I help you today?
        </h2>
        <p className="text-muted-foreground text-sm mb-8">
          I'm Jarvis, your intelligent assistant. Ask me anything or try one of these suggestions.
        </p>
        <div className="grid gap-2">
          {suggestions.map((s) => (
            <motion.button
              key={s.text}
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => onSuggestion(s.text)}
              className="flex items-center gap-3 px-4 py-3 rounded-xl border border-border bg-card hover:bg-secondary/50 transition-colors text-sm text-left"
            >
              <s.icon className={`w-4 h-4 ${s.color} shrink-0`} />
              <span className="text-foreground">{s.text}</span>
            </motion.button>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
