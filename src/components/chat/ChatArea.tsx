import { useRef, useEffect } from "react";
import { Menu, Settings } from "lucide-react";
import type { Conversation, Settings as SettingsType } from "@/types/chat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { ChatInput } from "./ChatInput";
import { EmptyState } from "./EmptyState";

interface Props {
  conversation: Conversation | null;
  isGenerating: boolean;
  onSend: (content: string) => void;
  onToggleSidebar: () => void;
  onOpenSettings: () => void;
  settings: SettingsType;
}

export function ChatArea({ conversation, isGenerating, onSend, onToggleSidebar, onOpenSettings, settings }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [conversation?.messages, isGenerating]);

  const hasMessages = conversation && conversation.messages.length > 0;

  return (
    <div className="flex-1 flex flex-col min-w-0">
      {/* Header */}
      <header className="h-14 flex items-center px-4 border-b border-border bg-background/80 backdrop-blur-sm shrink-0">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg hover:bg-secondary transition-colors md:hidden"
        >
          <Menu className="w-5 h-5 text-foreground" />
        </button>
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-lg hover:bg-secondary transition-colors hidden md:block"
        >
          <Menu className="w-5 h-5 text-foreground" />
        </button>
        <h2 className="ml-2 text-sm font-medium text-foreground truncate">
          {conversation?.title || "JarvisAI"}
        </h2>
        <div className="ml-auto flex items-center gap-2">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
            <span className="text-xs text-muted-foreground">{settings.model}</span>
          </span>
          <button
            onClick={onOpenSettings}
            className="p-2 rounded-lg hover:bg-secondary transition-colors"
          >
            <Settings className="w-4 h-4 text-muted-foreground" />
          </button>
        </div>
      </header>

      {/* Messages */}
      {hasMessages ? (
        <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin py-4">
          <div className="max-w-3xl mx-auto">
            {conversation.messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {isGenerating && <TypingIndicator />}
          </div>
        </div>
      ) : (
        <EmptyState onSuggestion={onSend} />
      )}

      {/* Input */}
      <ChatInput onSend={onSend} disabled={isGenerating} />
    </div>
  );
}
