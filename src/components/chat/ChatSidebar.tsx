import { Plus, MessageSquare, Trash2, Edit3, Check, X, Sun, Moon, Bot, Settings } from "lucide-react";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { Conversation, Theme } from "@/types/chat";

interface Props {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onCreate: () => void;
  onDelete: (id: string) => void;
  onRename: (id: string, title: string) => void;
  theme: Theme;
  onToggleTheme: () => void;
  isOpen: boolean;
  onClose: () => void;
  onOpenSettings: () => void;
}

export function ChatSidebar({
  conversations,
  activeId,
  onSelect,
  onCreate,
  onDelete,
  onRename,
  theme,
  onToggleTheme,
  isOpen,
  onClose,
  onOpenSettings,
}: Props) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState("");

  const startEdit = (id: string, title: string) => {
    setEditingId(id);
    setEditTitle(title);
  };

  const confirmEdit = (id: string) => {
    if (editTitle.trim()) onRename(id, editTitle.trim());
    setEditingId(null);
  };

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-jarvis-deep/60 backdrop-blur-sm z-40 md:hidden"
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      <motion.aside
        initial={false}
        animate={{ x: isOpen ? 0 : "-100%" }}
        transition={{ type: "spring", damping: 25, stiffness: 300 }}
        className="fixed md:relative z-50 md:z-auto h-full w-72 flex flex-col bg-sidebar border-r border-sidebar-border md:translate-x-0"
        style={{ translateX: undefined }}
      >
        {/* Header */}
        <div className="p-4 border-b border-sidebar-border">
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            <h1 className="font-semibold text-lg text-sidebar-foreground tracking-tight">
              Jarvis<span className="text-primary">AI</span>
            </h1>
          </div>
          <button
            onClick={onCreate}
            className="w-full flex items-center gap-2 px-3 py-2.5 rounded-lg bg-primary text-primary-foreground font-medium text-sm hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" />
            New Chat
          </button>
        </div>

        {/* Chat list */}
        <div className="flex-1 overflow-y-auto scrollbar-thin p-2 space-y-0.5">
          <AnimatePresence>
            {conversations.map((convo) => (
              <motion.div
                key={convo.id}
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className={`group flex items-center gap-2 px-3 py-2.5 rounded-lg cursor-pointer transition-colors text-sm ${
                  convo.id === activeId
                    ? "bg-sidebar-accent text-sidebar-accent-foreground"
                    : "text-sidebar-foreground hover:bg-sidebar-accent/50"
                }`}
                onClick={() => {
                  onSelect(convo.id);
                  onClose();
                }}
              >
                <MessageSquare className="w-4 h-4 shrink-0 text-muted-foreground" />
                {editingId === convo.id ? (
                  <div className="flex-1 flex items-center gap-1">
                    <input
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && confirmEdit(convo.id)}
                      className="flex-1 bg-background px-2 py-0.5 rounded text-sm border border-border outline-none focus:ring-1 focus:ring-primary"
                      autoFocus
                      onClick={(e) => e.stopPropagation()}
                    />
                    <button onClick={(e) => { e.stopPropagation(); confirmEdit(convo.id); }}>
                      <Check className="w-3.5 h-3.5 text-primary" />
                    </button>
                    <button onClick={(e) => { e.stopPropagation(); setEditingId(null); }}>
                      <X className="w-3.5 h-3.5 text-muted-foreground" />
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="flex-1 truncate">{convo.title}</span>
                    <div className="hidden group-hover:flex items-center gap-0.5">
                      <button
                        onClick={(e) => { e.stopPropagation(); startEdit(convo.id, convo.title); }}
                        className="p-1 rounded hover:bg-background/50"
                      >
                        <Edit3 className="w-3.5 h-3.5 text-muted-foreground" />
                      </button>
                      <button
                        onClick={(e) => { e.stopPropagation(); onDelete(convo.id); }}
                        className="p-1 rounded hover:bg-destructive/10"
                      >
                        <Trash2 className="w-3.5 h-3.5 text-destructive" />
                      </button>
                    </div>
                  </>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
          {conversations.length === 0 && (
            <p className="text-center text-muted-foreground text-xs mt-8 px-4">
              No conversations yet. Start a new chat!
            </p>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-sidebar-border space-y-0.5">
          <button
            onClick={onOpenSettings}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors"
          >
            <Settings className="w-4 h-4" />
            Settings
          </button>
          <button
            onClick={onToggleTheme}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm text-sidebar-foreground hover:bg-sidebar-accent/50 transition-colors"
          >
            {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            {theme === "dark" ? "Light Mode" : "Dark Mode"}
          </button>
        </div>
      </motion.aside>
    </>
  );
}
