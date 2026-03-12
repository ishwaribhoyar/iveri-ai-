export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

export type Theme = "light" | "dark";

export interface Settings {
  voiceEnabled: boolean;
  voiceSpeed: number;
  model: string;
  systemPrompt: string;
  temperature: number;
  maxTokens: number;
  streamResponses: boolean;
}

export const DEFAULT_SETTINGS: Settings = {
  voiceEnabled: false,
  voiceSpeed: 1.0,
  model: "sarvam-m",
  systemPrompt: "You are Jarvis, an intelligent AI assistant. You are helpful, concise, and knowledgeable. You can assist with general questions, coding, writing, analysis, and system automation when connected to a backend.",
  temperature: 0.7,
  maxTokens: 2048,
  streamResponses: false,
};

export const AVAILABLE_MODELS = [
  { id: "sarvam-m", name: "Sarvam M", description: "Primary model — balanced speed & quality" },
  { id: "sarvam-m-lite", name: "Sarvam M Lite", description: "Faster responses, lighter reasoning" },
  { id: "sarvam-m-pro", name: "Sarvam M Pro", description: "Advanced reasoning, slower" },
  { id: "local-llama", name: "Local LLaMA", description: "Offline — requires local server" },
];
