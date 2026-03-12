# Jarvis Core AI — Complete Project Deep Dive

## 1. Project Overview

**Jarvis Core AI** is a **frontend-only** intelligent AI chat assistant web application inspired by Jarvis from Iron Man. It is built using modern web technologies and currently functions as a **demo/prototype** with simulated AI responses. The project is specifically designed to be connected to a **backend API** (e.g., FastAPI with Sarvam AI models) to unlock its full potential — including real AI inference, voice recognition, voice output, and system automation.

**Live Dev Server:** Runs on `http://localhost:8080/` via Vite.

---

## 2. Tech Stack

| Layer         | Technology                                   |
|---------------|----------------------------------------------|
| Build Tool    | Vite v5.4.19 (with SWC for fast React compilation) |
| Language      | TypeScript (strict mode)                    |
| Framework     | React 18.3.1                                |
| Routing       | React Router DOM v6.30.1                    |
| Styling       | Tailwind CSS v3.4.17 + custom CSS variables |
| UI Components | shadcn/ui (49 Radix-based components)       |
| Animations    | Framer Motion v12.35.0                      |
| Markdown      | react-markdown v10.1.0 + remark-gfm v4.0.1 |
| Code Highlighting | react-syntax-highlighter (Prism + oneDark theme) |
| State Mgmt    | React hooks (useState, useCallback, useEffect) — no Redux/Zustand |
| Data Fetching | TanStack React Query v5.83.0 (set up but not actively used yet) |
| ID Generation | uuid v13.0.0                                |
| Persistence   | Browser localStorage                        |
| Icons         | Lucide React v0.462.0                       |
| Fonts         | Inter (UI) + JetBrains Mono (code)          |
| Testing       | Vitest + Testing Library + jsdom            |
| Linting       | ESLint v9 + React Hooks plugin              |
| Package Mgr   | npm (also has bun.lock)                     |

---

## 3. Project Structure

```
jarvis-core-ai/
├── index.html                   # Entry HTML (title: "JarvisAI — Intelligent Assistant")
├── vite.config.ts               # Vite config (port 8080, path alias @/ → ./src)
├── tailwind.config.ts           # Tailwind config with custom Jarvis theme
├── tsconfig.json                # TypeScript project config
├── tsconfig.app.json            # App-specific TS config
├── tsconfig.node.json           # Node-specific TS config
├── postcss.config.js            # PostCSS (autoprefixer + tailwindcss)
├── eslint.config.js             # ESLint config
├── components.json              # shadcn/ui config
├── package.json                 # Dependencies & scripts
│
├── public/                      # Static assets
│
└── src/
    ├── main.tsx                 # React entry point (renders <App />)
    ├── App.tsx                  # Root component (routing + providers)
    ├── App.css                  # App-level styles
    ├── index.css                # Global CSS + design system tokens
    ├── vite-env.d.ts            # Vite type declarations
    │
    ├── pages/
    │   ├── Index.tsx            # Main page — chat interface (only page)
    │   └── NotFound.tsx         # 404 catch-all page
    │
    ├── components/
    │   ├── NavLink.tsx          # Navigation link component
    │   ├── chat/
    │   │   ├── ChatArea.tsx     # Main chat view (messages + input)
    │   │   ├── ChatInput.tsx    # Message input with mic button
    │   │   ├── ChatSidebar.tsx  # Conversation list sidebar
    │   │   ├── MessageBubble.tsx # Individual message with markdown rendering
    │   │   ├── EmptyState.tsx   # Welcome screen with suggestion buttons
    │   │   ├── SettingsPanel.tsx # Settings slide-over panel
    │   │   └── TypingIndicator.tsx # Animated "AI is typing" dots
    │   └── ui/                  # 49 shadcn/ui components (button, dialog, etc.)
    │
    ├── hooks/
    │   ├── useChatStore.ts      # Chat state management (conversations, messages)
    │   ├── useSettings.ts       # Settings state management
    │   ├── useTheme.ts          # Dark/light theme management
    │   ├── use-mobile.tsx       # Mobile breakpoint detection
    │   └── use-toast.ts         # Toast notification hook
    │
    ├── types/
    │   └── chat.ts              # TypeScript interfaces & constants
    │
    ├── lib/
    │   └── utils.ts             # Utility functions (cn helper)
    │
    └── test/
        ├── setup.ts             # Test configuration
        └── example.test.ts      # Example test file
```

---

## 4. Detailed Architecture

### 4.1 Application Entry & Routing

**`main.tsx`** renders `<App />` into `div#root`.

**`App.tsx`** sets up the application shell with these providers (outermost → innermost):
1. **`QueryClientProvider`** — TanStack React Query (ready for backend API calls)
2. **`TooltipProvider`** — Global tooltip support
3. **`Toaster`** + **`Sonner`** — Dual toast/notification systems
4. **`BrowserRouter`** — Client-side routing

**Routes:**
| Path  | Component   | Description                  |
|-------|-------------|------------------------------|
| `/`   | `<Index />` | Main chat interface          |
| `*`   | `<NotFound />` | 404 catch-all              |

### 4.2 Main Page (`Index.tsx`)

The Index page is the **only real page** — a full-screen chat interface. It composes three main areas:

```
┌──────────────────────────────────────────────────────┐
│ ┌──────────┐ ┌─────────────────────────┐ ┌────────┐ │
│ │          │ │                         │ │Settings│ │
│ │ Chat     │ │      ChatArea           │ │Panel   │ │
│ │ Sidebar  │ │  (messages + input)     │ │(slide  │ │
│ │ (convos) │ │                         │ │ over)  │ │
│ │          │ │                         │ │        │ │
│ └──────────┘ └─────────────────────────┘ └────────┘ │
└──────────────────────────────────────────────────────┘
```

It instantiates three hooks:
- `useTheme()` → `{ theme, toggleTheme }`
- `useSettings()` → `{ settings, updateSettings, resetSettings }`
- `useChatStore()` → `{ conversations, activeConversation, activeId, isGenerating, setActiveId, createConversation, deleteConversation, renameConversation, sendMessage }`

---

## 5. TypeScript Interfaces & Data Models

### 5.1 `Message`
```typescript
interface Message {
  id: string;          // UUID v4
  role: "user" | "assistant";
  content: string;     // Supports markdown
  timestamp: number;   // Unix ms
}
```

### 5.2 `Conversation`
```typescript
interface Conversation {
  id: string;          // UUID v4
  title: string;       // Auto-set from first message (first 40 chars)
  messages: Message[];
  createdAt: number;   // Unix ms
  updatedAt: number;   // Unix ms
}
```

### 5.3 `Settings`
```typescript
interface Settings {
  voiceEnabled: boolean;      // default: false
  voiceSpeed: number;         // default: 1.0 (range: 0.5 – 2.0)
  model: string;              // default: "sarvam-m"
  systemPrompt: string;       // default: "You are Jarvis, an intelligent AI assistant..."
  temperature: number;        // default: 0.7 (range: 0 – 2.0)
  maxTokens: number;          // default: 2048 (range: 256 – 8192)
  streamResponses: boolean;   // default: true
}
```

### 5.4 Available AI Models (defined in frontend)
```typescript
const AVAILABLE_MODELS = [
  { id: "sarvam-m",     name: "Sarvam M",      description: "Primary model — balanced speed & quality" },
  { id: "sarvam-m-lite", name: "Sarvam M Lite", description: "Faster responses, lighter reasoning" },
  { id: "sarvam-m-pro", name: "Sarvam M Pro",   description: "Advanced reasoning, slower" },
  { id: "local-llama",  name: "Local LLaMA",    description: "Offline — requires local server" },
];
```

### 5.5 Theme
```typescript
type Theme = "light" | "dark";
```

---

## 6. State Management (Custom React Hooks)

### 6.1 `useChatStore()` — Core Chat Logic

**Storage:** `localStorage` key = `"jarvis-conversations"`

**Current behavior (DEMO MODE — no backend):**
- Conversations are stored as a JSON array in localStorage
- When user sends a message, a **simulated AI response** is generated after a random delay (800–2000ms)
- The demo `generateResponse()` function pattern-matches keywords ("hello", "code", "help", "who are you") to return canned markdown responses
- For unrecognized input, it picks a random generic response from a pool of 4

**Exposed API:**
| Method | Signature | Description |
|--------|-----------|-------------|
| `conversations` | `Conversation[]` | All stored conversations |
| `activeConversation` | `Conversation \| null` | Currently selected conversation |
| `activeId` | `string \| null` | ID of active conversation |
| `isGenerating` | `boolean` | Whether AI is "thinking" |
| `setActiveId` | `(id: string) => void` | Switch active conversation |
| `createConversation` | `() => string` | Create new empty conversation, returns ID |
| `deleteConversation` | `(id: string) => void` | Delete a conversation |
| `renameConversation` | `(id: string, title: string) => void` | Rename a conversation |
| `sendMessage` | `(content: string) => Promise<void>` | Send message + generate AI response |

**What needs to change for backend integration:**
- Replace `generateResponse()` with an actual HTTP call to the backend API
- Support streaming responses (SSE/WebSocket) for real-time token display
- The `sendMessage` function should POST to a `/chat` endpoint

### 6.2 `useSettings()` — Settings Persistence

**Storage:** `localStorage` key = `"jarvis-settings"`

Merges stored settings with defaults on load, so new settings fields are automatically supported.

**Exposed API:**
| Method | Description |
|--------|-------------|
| `settings` | Current settings object |
| `updateSettings(partial)` | Merge partial settings update |
| `resetSettings()` | Reset to `DEFAULT_SETTINGS` |

**What needs to change for backend integration:**
- Settings like `model`, `temperature`, `maxTokens`, `systemPrompt`, and `streamResponses` need to be sent with each API request to the backend
- `voiceEnabled` and `voiceSpeed` should trigger the backend's TTS endpoint

### 6.3 `useTheme()` — Theme Management

**Storage:** `localStorage` key = `"jarvis-theme"`

- Auto-detects system preference on first load
- Toggles `dark` class on `<html>` element
- Uses Tailwind's `darkMode: ["class"]` strategy

---

## 7. Component Details

### 7.1 `ChatSidebar`
- Left panel (width: `w-72`, 288px)
- Shows JarvisAI branding with Bot icon
- "New Chat" button to create conversations
- Lists all conversations with:
  - Inline rename (edit icon → input field)
  - Delete button (trash icon, appears on hover)
  - Active conversation highlighting
- Footer has: Settings button + Theme toggle (Sun/Moon)
- On mobile: slides in as overlay with backdrop blur
- Animated with Framer Motion (spring animation for open/close)

### 7.2 `ChatArea`
- Header bar showing:
  - Hamburger menu (toggle sidebar)
  - Conversation title
  - Active model indicator with pulsing green dot
  - Settings gear icon
- Message list (auto-scrolls to bottom on new messages)
- Shows `EmptyState` when no messages exist
- Shows `TypingIndicator` when AI is generating
- `ChatInput` at the bottom

### 7.3 `ChatInput`
- Auto-resizing `<textarea>` (max 160px height)
- Mic button (non-functional — placeholder for voice input, needs backend)
- Send button with Framer Motion tap animation
- Enter to send, Shift+Enter for newline
- Disabled state while AI is generating
- Footer text: "Jarvis can make mistakes. Connect to a backend for full capabilities."

### 7.4 `MessageBubble`
- User messages: teal/cyan bubble on the right, plain text with User icon
- AI messages: gray bubble on the left, with Bot icon
- AI messages render **full Markdown** via `react-markdown` + `remark-gfm`:
  - Headers, bold, italic, links, blockquotes
  - Bullet/numbered lists
  - Tables with styled headers
  - **Code blocks** with:
    - Language label (e.g., "typescript")
    - Copy button
    - Prism syntax highlighting (oneDark theme)
  - Inline code with styled background
- Copy-to-clipboard button on hover (for entire AI message)
- Animated entrance via Framer Motion (fade + slide up)
- Memoized with `React.memo` for performance

### 7.5 `EmptyState`
- Centered welcome screen with:
  - Large Bot icon with glow effect
  - "How can I help you today?" heading
  - 3 suggestion buttons:
    1. "Tell me about yourself"
    2. "Show me a code example"
    3. "What can you help me with?"
  - Clicking a suggestion sends it as a message

### 7.6 `SettingsPanel`
- Slide-over panel from the right (max width 448px)
- Backdrop blur overlay
- Sections:
  1. **Voice** — Toggle voice output on/off + voice speed slider (0.5x–2.0x)
  2. **Model** — Select from 4 models (Sarvam M, M Lite, M Pro, Local LLaMA)
  3. **Temperature** — Slider (0.0 "Precise" to 2.0 "Creative")
  4. **Max Tokens** — Slider (256 to 8192, step 256)
  5. **Stream Responses** — Toggle for streaming token display
  6. **System Prompt** — Editable textarea with character count & reset button
- Reset to defaults button in header
- Footer: "Settings are saved locally and apply to all conversations."

### 7.7 `TypingIndicator`
- Three animated dots with staggered bouncing animation
- Bot icon on the left
- CSS animation: `typing-dot` keyframes (1.4s cycle)

---

## 8. Design System & Theming

### 8.1 CSS Custom Properties

The project uses **HSL-based CSS custom properties** for full light/dark mode support. All colors are defined in `index.css` as `@layer base` variables.

**Key color tokens:**
| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--background` | Light gray | Very dark blue | Page background |
| `--foreground` | Near black | Light gray | Text color |
| `--primary` | Teal (185° 80% 40%) | Bright teal (185° 85% 50%) | Accent, buttons, links |
| `--user-bubble` | Teal (185° 75% 42%) | Teal (185° 80% 45%) | User message bubbles |
| `--ai-bubble` | Light gray | Dark gray | AI message bubbles |
| `--code-bg` | Very dark | Very dark | Code block background |
| `--jarvis-glow` | Teal glow | Brighter teal glow | Glow effects |
| `--jarvis-deep` | Near black | Very dark | Overlay backgrounds |

### 8.2 Custom Tailwind Extensions
- **Colors:** `jarvis.glow`, `jarvis.surface`, `jarvis.deep`, `user-bubble`, `ai-bubble`, `code-bg`
- **Animations:** `pulse-glow` (2s pulsing opacity), `typing-dot` (1.4s bouncing dots)
- **Utilities:** `.glow-primary`, `.glow-text`, `.scrollbar-thin`

### 8.3 Typography
- **UI:** Inter (weights: 300–700)
- **Code:** JetBrains Mono (weights: 400–700)
- Both loaded from Google Fonts

### 8.4 Markdown Prose Styling
Custom `.prose-jarvis` class with styles for: headings, paragraphs, lists, inline code, links, blockquotes, tables.

---

## 9. What Currently Works (Frontend Demo)

| Feature | Status | Details |
|---------|--------|---------|
| Multi-conversation management | ✅ Working | Create, delete, rename, switch between conversations |
| Message sending & display | ✅ Working | User messages with typing, AI simulated responses |
| Markdown rendering | ✅ Working | Full GFM with tables, code blocks, blockquotes |
| Code syntax highlighting | ✅ Working | Prism-based with 100+ language support |
| Copy to clipboard | ✅ Working | Copy code blocks and full AI messages |
| Dark/Light theme | ✅ Working | Persistent toggle, auto-detects system preference |
| Settings panel | ✅ Working | All UI controls work, settings persist in localStorage |
| Responsive design | ✅ Working | Mobile sidebar overlay, responsive layout |
| Conversation persistence | ✅ Working | All conversations saved in localStorage |
| Typing indicator animation | ✅ Working | Animated dots while AI is "generating" |
| Smooth animations | ✅ Working | Framer Motion throughout UI |
| Voice input (Mic button) | ❌ Not Connected | Button exists, needs backend Speech-to-Text |
| Voice output (TTS) | ❌ Not Connected | Setting exists, needs backend Text-to-Speech |
| Actual AI responses | ❌ Not Connected | Currently uses hardcoded demo responses |
| Streaming responses | ❌ Not Connected | Toggle exists, needs backend SSE/WebSocket |
| System automation | ❌ Not Connected | Mentioned in UI, needs backend implementation |
| Model selection effect | ❌ Not Connected | UI works, but model choice has no real effect |

---

## 10. What the Backend Needs to Provide

### 10.1 Core Chat API

**Endpoint:** `POST /api/chat`

**Request body the frontend is ready to send:**
```json
{
  "message": "user text here",
  "conversation_id": "uuid",
  "model": "sarvam-m",
  "system_prompt": "You are Jarvis...",
  "temperature": 0.7,
  "max_tokens": 2048,
  "stream": true
}
```

**Expected response (non-streaming):**
```json
{
  "id": "msg-uuid",
  "role": "assistant",
  "content": "AI response in markdown",
  "timestamp": 1709654321000
}
```

**Expected response (streaming):**
Server-Sent Events (SSE) or WebSocket with chunks:
```
data: {"delta": "Here's", "done": false}
data: {"delta": " my", "done": false}
data: {"delta": " response.", "done": true}
```

### 10.2 Voice / Speech API

**Speech-to-Text (STT):**
- Endpoint: `POST /api/voice/stt`
- Input: Audio blob (WebM/WAV from browser MediaRecorder)
- Output: `{ "text": "transcribed text" }`
- Frontend mic button needs to be connected to record audio and POST it

**Text-to-Speech (TTS):**
- Endpoint: `POST /api/voice/tts`
- Input: `{ "text": "AI response text", "speed": 1.0 }`
- Output: Audio blob for playback
- Triggered when `voiceEnabled` is true in settings

### 10.3 System Automation API (Optional/Advanced)

- Endpoint: `POST /api/system/execute`
- Input: `{ "command": "open notepad" }` or structured action objects
- Output: `{ "success": true, "output": "..." }`
- The AI model should determine when to trigger system commands from chat

### 10.4 Conversation History API (Optional Enhancement)

Currently conversations are stored only in localStorage. Backend could provide:
- `GET /api/conversations` — List all conversations
- `GET /api/conversations/:id` — Get conversation with messages
- `POST /api/conversations` — Create new conversation
- `DELETE /api/conversations/:id` — Delete conversation
- This would enable cross-device sync and server-side persistence

---

## 11. Frontend Integration Points (Where to Connect Backend)

### 11.1 Primary: `useChatStore.ts` → `sendMessage()` function

**Current code (lines 92–134) — replace the simulated logic:**
```typescript
// CURRENT (demo mode):
await new Promise((r) => setTimeout(r, 800 + Math.random() * 1200));
const response = generateResponse(content);

// SHOULD BECOME:
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: content,
    conversation_id: targetId,
    model: settings.model,
    system_prompt: settings.systemPrompt,
    temperature: settings.temperature,
    max_tokens: settings.maxTokens,
    stream: settings.streamResponses,
  }),
});
```

For streaming, use `EventSource` or `fetch` with `ReadableStream` to receive tokens incrementally.

### 11.2 Voice: `ChatInput.tsx` → Mic button (line 39–44)

The mic button currently does nothing. Needs:
1. `navigator.mediaDevices.getUserMedia({ audio: true })` to capture audio
2. `MediaRecorder` to record audio chunks
3. POST audio blob to `/api/voice/stt`
4. Auto-fill the text input with transcribed text

### 11.3 Voice Output: `MessageBubble.tsx` or `useChatStore.ts`

After receiving an AI response, if `settings.voiceEnabled` is true:
1. POST response text to `/api/voice/tts`
2. Play returned audio using `new Audio(blobUrl).play()`

### 11.4 Settings: Need to be passed with every API call

The `useSettings()` hook already manages: `model`, `temperature`, `maxTokens`, `systemPrompt`, `streamResponses`, `voiceEnabled`, `voiceSpeed` — all need to be included in backend requests.

---

## 12. Key Design Decisions & Patterns

1. **No global state library** — Pure React hooks (useState, useCallback) for all state
2. **Local-first** — Everything persists in localStorage; backend is optional enhancement
3. **Settings merged with defaults** — New settings fields automatically get defaults
4. **Memoized components** — `MessageBubble` uses `React.memo` to avoid re-renders
5. **Path alias** — `@/` maps to `./src/` for clean imports
6. **shadcn/ui pattern** — UI primitives are in `components/ui/`, copied (not imported from package)
7. **CSS variables for theming** — All colors use HSL variables, enabling runtime theme switching
8. **Responsive first** — Sidebar collapses on mobile, input area adapts
9. **Animation throughout** — Framer Motion for sidebar, messages, buttons, panels

---

## 13. NPM Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `dev` | `vite` | Start dev server on port 8080 |
| `build` | `vite build` | Production build |
| `build:dev` | `vite build --mode development` | Dev build |
| `preview` | `vite preview` | Preview production build |
| `lint` | `eslint .` | Run ESLint |
| `test` | `vitest run` | Run tests once |
| `test:watch` | `vitest` | Run tests in watch mode |

---

## 14. Summary for Backend Developer

**You are building a backend for a fully-featured AI chat assistant frontend.** The frontend is complete with:

- A polished chat UI with conversation management
- Markdown + code syntax highlighting in message bubbles
- Settings panel with model selection, temperature, max tokens, system prompt, voice, and streaming toggles
- Dark/light theme
- Voice input button (mic icon — needs STT backend)
- Voice output toggle (needs TTS backend)
- Streaming response toggle (needs SSE/WebSocket backend)

**Your backend should:**
1. Expose a `POST /api/chat` endpoint that accepts messages with model/settings params and returns AI responses (support both streaming and non-streaming)
2. Integrate with **Sarvam AI** models (sarvam-m, sarvam-m-lite, sarvam-m-pro) or a local LLaMA server
3. Provide `POST /api/voice/stt` for speech-to-text (mic input)
4. Provide `POST /api/voice/tts` for text-to-speech (voice output)
5. Optionally support system automation commands via `POST /api/system/execute`
6. Optionally provide conversation CRUD endpoints for server-side persistence
7. Handle CORS for `http://localhost:8080` (the Vite dev server)
8. The frontend will send: `message`, `conversation_id`, `model`, `system_prompt`, `temperature`, `max_tokens`, `stream` with each chat request
