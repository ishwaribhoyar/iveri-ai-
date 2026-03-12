# Iveri AI — Intelligent Assistant

An AI-powered assistant with chat, voice, and system automation capabilities. Built with React + Vite (frontend) and FastAPI (backend), powered by Sarvam AI.

## Features

- 🤖 **AI Chat** — Powered by Sarvam AI with markdown rendering and code highlighting
- 🎤 **Voice** — Speech-to-text and text-to-speech support
- ⚡ **System Automation** — Open apps, websites, YouTube search, take screenshots
- 🌙 **Dark/Light Mode** — Beautiful, responsive UI
- 📱 **Cross-Platform** — Deploy anywhere with Vercel + Render

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend  | React 18, TypeScript, Vite, Tailwind CSS |
| Backend   | Python, FastAPI, Uvicorn |
| AI Model  | Sarvam AI (sarvam-m) |
| Database  | SQLite (aiosqlite) |
| Deploy    | Vercel (frontend), Render (backend) |

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Sarvam AI API key

### Installation

```bash
# Clone the repo
git clone https://github.com/ishwaribhoyar/Iveri-AI.git
cd Iveri-AI

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your SARVAM_API_KEY
```

### Running Locally

```bash
# Terminal 1 — Backend
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend
npm run dev
```

Open http://localhost:8080 in your browser.

## Deployment

- **Frontend**: Deploy to [Vercel](https://vercel.com) — auto-detects Vite
- **Backend**: Deploy to [Render](https://render.com) — uses `render.yaml` blueprint

See `backend/.env.example` for required environment variables.

## Author

**Ishwari Bhoyar** — [@ishwaribhoyar](https://github.com/ishwaribhoyar)
