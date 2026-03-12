import { useState, useCallback, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import type { Conversation, Message, Settings } from "@/types/chat";

const STORAGE_KEY = "jarvis-conversations";

// API base URL — uses Vite proxy in dev, Vercel rewrites in prod
const API_BASE = import.meta.env.VITE_API_URL || "/api";

/** Strip <think>...</think> reasoning blocks from AI output */
function stripThinkTags(text: string): string {
  let cleaned = text.replace(/<think>[\s\S]*?<\/think>/g, "");
  // Handle unclosed think tags
  cleaned = cleaned.replace(/<think>[\s\S]*$/g, "");
  cleaned = cleaned.trim();
  // If stripping left nothing, just remove the tags but keep content
  if (!cleaned) {
    return text.replace(/<\/?think>/g, "").trim();
  }
  return cleaned;
}

function loadConversations(): Conversation[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveConversations(convos: Conversation[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convos));
}

export function useChatStore(settings?: Settings) {
  const [conversations, setConversations] = useState<Conversation[]>(loadConversations);
  const [activeId, setActiveId] = useState<string | null>(() => {
    const convos = loadConversations();
    return convos.length > 0 ? convos[0].id : null;
  });
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    saveConversations(conversations);
  }, [conversations]);

  const activeConversation = conversations.find((c) => c.id === activeId) ?? null;

  const createConversation = useCallback(() => {
    const convo: Conversation = {
      id: uuidv4(),
      title: "New Chat",
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    setConversations((prev) => [convo, ...prev]);
    setActiveId(convo.id);
    return convo.id;
  }, []);

  const deleteConversation = useCallback(
    (id: string) => {
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (activeId === id) {
        setActiveId((prev) => {
          const remaining = conversations.filter((c) => c.id !== id);
          return remaining.length > 0 ? remaining[0].id : null;
        });
      }
    },
    [activeId, conversations]
  );

  const renameConversation = useCallback((id: string, title: string) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? { ...c, title, updatedAt: Date.now() } : c))
    );
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      let targetId = activeId;
      if (!targetId) {
        const convo: Conversation = {
          id: uuidv4(),
          title: content.slice(0, 40) || "New Chat",
          messages: [],
          createdAt: Date.now(),
          updatedAt: Date.now(),
        };
        setConversations((prev) => [convo, ...prev]);
        targetId = convo.id;
        setActiveId(targetId);
      }

      const userMsg: Message = { id: uuidv4(), role: "user", content, timestamp: Date.now() };

      setConversations((prev) =>
        prev.map((c) => {
          if (c.id !== targetId) return c;
          const updated = { ...c, messages: [...c.messages, userMsg], updatedAt: Date.now() };
          if (c.messages.length === 0) updated.title = content.slice(0, 40);
          return updated;
        })
      );

      setIsGenerating(true);

      // Force non-streaming: Sarvam AI wraps responses in <think> tags
      // which breaks the streaming UX. Non-streaming works perfectly.
      const shouldStream = false;

      try {
        const body = {
          message: content,
          conversation_id: targetId,
          model: settings?.model ?? "sarvam-m",
          system_prompt: settings?.systemPrompt ?? "You are Jarvis, an intelligent AI assistant.",
          temperature: settings?.temperature ?? 0.7,
          max_tokens: settings?.maxTokens ?? 2048,
          stream: false,
        };

        console.log("[Jarvis] Sending chat request:", body.message);

        const resp = await fetch(`${API_BASE}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });

        console.log("[Jarvis] Response status:", resp.status);

        if (!resp.ok) {
          throw new Error(`Server error: ${resp.status}`);
        }

        const data = await resp.json();
        console.log("[Jarvis] Response data:", data);

        // Clean any <think> tags from the response
        let responseContent = data.content || "";
        responseContent = responseContent.replace(/<think>[\s\S]*?<\/think>/g, "").trim();
        if (!responseContent) {
          responseContent = (data.content || "").replace(/<\/?think>/g, "").trim();
        }
        if (!responseContent) {
          responseContent = "I received your message but couldn't generate a proper response. Please try again.";
        }

        console.log("[Jarvis] Clean content:", responseContent.substring(0, 100));

        const aiMsg: Message = {
          id: data.id || uuidv4(),
          role: "assistant",
          content: responseContent,
          timestamp: data.timestamp || Date.now(),
        };

        setConversations((prev) =>
          prev.map((c) =>
            c.id === targetId
              ? { ...c, messages: [...c.messages, aiMsg], updatedAt: Date.now() }
              : c
          )
        );
      } catch (error) {
        console.error("[Jarvis] Chat API error:", error);
        const errorMsg: Message = {
          id: uuidv4(),
          role: "assistant",
          content: `⚠️ **Connection Error**\n\nCould not reach the backend server. Please ensure:\n\n1. The backend is running: \`cd backend && python app.py\`\n2. It's accessible at \`http://localhost:8000\`\n\nError: ${error}`,
          timestamp: Date.now(),
        };
        setConversations((prev) =>
          prev.map((c) =>
            c.id === targetId
              ? { ...c, messages: [...c.messages, errorMsg], updatedAt: Date.now() }
              : c
          )
        );
      }

      setIsGenerating(false);
    },
    [activeId, settings]
  );

  return {
    conversations,
    activeConversation,
    activeId,
    isGenerating,
    setActiveId,
    createConversation,
    deleteConversation,
    renameConversation,
    sendMessage,
  };
}
