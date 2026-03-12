<div align="center">

# 🤖 Iveri AI

### _Your Intelligent AI Assistant — Chat, Voice & System Automation_

[![Built with FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/Frontend-React_18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

<p align="center">
  <strong>A full-stack AI assistant</strong> that combines conversational AI, real-time voice interaction, and system automation into a single, beautifully crafted interface.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-deployment">Deployment</a> •
  <a href="#-contributing">Contributing</a>
</p>

<br/>

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 💬 Intelligent Chat
- Powered by **Sarvam AI** language model
- Full **Markdown rendering** with syntax highlighting
- Conversation history with **persistent storage**
- Think-tag filtering for clean responses
- Multi-model support (sarvam-m, lite, pro)

</td>
<td width="50%">

### 🎤 Voice Interface
- **Speech-to-Text** via Google Speech Recognition
- **Text-to-Speech** with adjustable speed
- Real-time audio processing
- Seamless voice-to-chat workflow

</td>
</tr>
<tr>
<td width="50%">

### ⚡ System Automation
- **Open apps**: Notepad, Calculator, VS Code, Chrome...
- **YouTube search**: "Play [song] on YouTube"
- **Google search**: "Search [topic]"
- **Social profiles**: "Open insta account of [user]"
- **System info**: CPU, RAM, battery, disk usage
- **Screenshots**: Capture screen instantly

</td>
<td width="50%">

### 🎨 Premium UI/UX
- **Dark/Light mode** with smooth transitions
- **Glassmorphism** design language
- **Responsive** — works on desktop & mobile
- **Micro-animations** with Framer Motion
- **Code blocks** with Prism.js syntax highlighting
- Built with **Tailwind CSS** + **shadcn/ui**

</td>
</tr>
</table>

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                     │
│                                                         │
│   React 18 + TypeScript + Vite + Tailwind CSS           │
│   ┌─────────┐  ┌──────────┐  ┌─────────────────────┐   │
│   │ChatArea │  │VoiceInput│  │  Settings/Sidebar    │   │
│   │         │  │  (STT)   │  │  (Theme, Model, etc) │   │
│   └────┬────┘  └────┬─────┘  └──────────┬──────────┘   │
│        │            │                    │              │
│        └────────────┼────────────────────┘              │
│                     │ fetch(/api/*)                     │
└─────────────────────┼───────────────────────────────────┘
                      │ HTTPS
┌─────────────────────┼───────────────────────────────────┐
│                 BACKEND (Render)                        │
│                     │                                   │
│   FastAPI + Uvicorn + Python 3.11                       │
│   ┌─────────────────▼──────────────────────────┐        │
│   │            API Router Layer                 │        │
│   │  /api/chat  /api/voice/*  /api/system/*    │        │
│   └──────┬──────────┬──────────────┬───────────┘        │
│          │          │              │                     │
│   ┌──────▼───┐ ┌────▼─────┐ ┌─────▼──────┐             │
│   │ Intent   │ │  Voice   │ │  System    │             │
│   │ Service  │ │ Service  │ │  Tools     │             │
│   └──────┬───┘ └──────────┘ └────────────┘             │
│          │                                              │
│   ┌──────▼──────────────────────────────────┐           │
│   │         Sarvam AI API (LLM)             │           │
│   └─────────────────────────────────────────┘           │
│                                                         │
│   ┌─────────────────────────────────────────┐           │
│   │         SQLite Database (aiosqlite)      │           │
│   │   Conversations │ Messages │ Events      │           │
│   └─────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, TypeScript | UI Components & State Management |
| **Styling** | Tailwind CSS, shadcn/ui | Design System & UI Primitives |
| **Bundler** | Vite 5 | Development & Production Builds |
| **Animations** | Framer Motion | Micro-interactions & Transitions |
| **Markdown** | react-markdown, remark-gfm | Rich Text Rendering |
| **Code Highlighting** | Prism.js (react-syntax-highlighter) | Code Block Rendering |
| **Backend** | FastAPI, Uvicorn | REST API Server |
| **AI Model** | Sarvam AI (sarvam-m) | Natural Language Processing |
| **Database** | SQLite (aiosqlite) | Async Persistent Storage |
| **Voice** | SpeechRecognition, pyttsx3 | STT & TTS Processing |
| **System** | psutil, pyautogui | System Monitoring & Automation |
| **Deployment** | Vercel + Render | Frontend CDN + Backend PaaS |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|------------|---------|
| Node.js | 18+ |
| Python | 3.11+ |
| npm | 9+ |
| Git | 2.x |

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/ishwaribhoyar/iveri-ai-.git
cd iveri-ai-

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create backend environment file
cp .env.example .env
```

Edit `backend/.env` with your API key:
```env
SARVAM_API_KEY=your_sarvam_api_key_here
FRONTEND_URL=http://localhost:8080
```

> 💡 **Get your API key** at [sarvam.ai](https://www.sarvam.ai/) — free tier available

### 3. Run Locally

```bash
# Terminal 1 — Start Backend
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Terminal 2 — Start Frontend
npm run dev
```

Open **http://localhost:8080** and start chatting! 🎉

---

## 📡 API Reference

### Chat

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/chat` | Send a message and get AI response |
| `GET` | `/api/health` | Health check & API key status |

#### `POST /api/chat`

```json
{
  "message": "Hello, tell me about AI",
  "conversation_id": "uuid-v4",
  "model": "sarvam-m",
  "system_prompt": "You are Jarvis, an intelligent assistant.",
  "temperature": 0.7,
  "max_tokens": 2048,
  "stream": false
}
```

**Response:**
```json
{
  "id": "msg-uuid",
  "role": "assistant",
  "content": "Hello! I'm Iveri AI, your intelligent assistant...",
  "timestamp": 1773052290364
}
```

### Voice

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/voice/stt` | Speech-to-Text (audio → text) |
| `POST` | `/api/voice/tts` | Text-to-Speech (text → WAV audio) |

### System

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/api/system/info` | System information (CPU, RAM, etc.) |
| `POST` | `/api/system/screenshot` | Capture screenshot |

---

## 🚢 Deployment

### Frontend → Vercel

1. Import repository at [vercel.com/new](https://vercel.com/new)
2. Framework auto-detected as **Vite**
3. Update `vercel.json` with your Render backend URL:
   ```json
   {
     "rewrites": [{
       "source": "/api/:path*",
       "destination": "https://YOUR-APP.onrender.com/api/:path*"
     }]
   }
   ```
4. Deploy! ✅

### Backend → Render

1. Create new **Web Service** at [render.com](https://render.com)
2. Connect your GitHub repository
3. Configure:
   | Setting | Value |
   |---------|-------|
   | **Root Directory** | `backend` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
4. Set environment variables:
   | Variable | Value |
   |----------|-------|
   | `SARVAM_API_KEY` | Your API key |
   | `FRONTEND_URL` | Your Vercel URL |
   | `PYTHON_VERSION` | `3.11.0` |
5. Deploy! ✅

---

## 📁 Project Structure

```
iveri-ai/
├── src/                          # Frontend source
│   ├── components/
│   │   └── chat/
│   │       ├── ChatArea.tsx      # Main chat view
│   │       ├── ChatInput.tsx     # Message input with voice
│   │       ├── MessageBubble.tsx # Message rendering (Markdown)
│   │       └── TypingIndicator.tsx
│   ├── hooks/
│   │   └── useChatStore.ts      # Chat state management
│   ├── pages/
│   │   └── Index.tsx             # Main application page
│   └── types/
│       └── chat.ts              # TypeScript interfaces
│
├── backend/                      # Backend source
│   ├── api/
│   │   ├── chat_routes.py       # Chat API endpoints
│   │   ├── voice_routes.py      # Voice API endpoints
│   │   └── system_routes.py     # System automation API
│   ├── services/
│   │   ├── sarvam_service.py    # Sarvam AI integration
│   │   ├── intent_service.py    # NLP intent detection
│   │   ├── stream_service.py    # SSE streaming
│   │   └── voice_service.py     # TTS/STT processing
│   ├── tools/
│   │   └── system_tools.py      # OS automation tools
│   ├── database/
│   │   └── database.py          # SQLite async database
│   ├── config/
│   │   └── settings.py          # Environment configuration
│   ├── app.py                   # FastAPI entry point
│   ├── requirements.txt         # Python dependencies
│   ├── render.yaml              # Render blueprint
│   └── Procfile                 # Process configuration
│
├── vercel.json                   # Vercel deployment config
├── vite.config.ts               # Vite configuration
├── tailwind.config.ts           # Tailwind CSS configuration
├── package.json                 # Node.js dependencies
└── README.md                    # You are here! 👋
```

---

## 🧠 Intent Detection

Iveri AI uses **intelligent pattern matching** to detect user intent and route commands:

```
User: "Play Shape of You on YouTube"
  → Intent: system_command
  → Action: open_website
  → URL: youtube.com/results?search_query=Shape+of+You

User: "Open insta account of virat.kohli"
  → Intent: system_command
  → Action: open_website
  → URL: instagram.com/virat.kohli

User: "What is machine learning?"
  → Intent: chat
  → Route: Sarvam AI for intelligent response
```

### Supported Commands

| Category | Example Commands |
|----------|-----------------|
| 🎵 **YouTube** | "Play Eminem on YouTube", "Search tutorials on YouTube" |
| 🔍 **Google** | "Search Python tutorials", "Google machine learning" |
| 📱 **Social Media** | "Open insta/twitter/github of [username]" |
| 💻 **Apps** | "Open notepad/calculator/chrome/vscode" |
| 🌐 **Websites** | "Open github.com", "Open gmail" |
| 📊 **System** | "System info", "Battery status", "CPU usage" |
| 📸 **Screenshot** | "Take screenshot", "Capture screen" |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Run frontend in dev mode (hot reload)
npm run dev

# Run backend in dev mode
cd backend && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Run frontend tests
npm test

# Run backend tests
cd backend && python test_api.py

# Type checking
npx tsc --noEmit
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ by [Ishwari Bhoyar](https://github.com/ishwaribhoyar)**

<br/>

<sub>If you found this project helpful, consider giving it a ⭐</sub>

</div>
