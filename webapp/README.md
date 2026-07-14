# PESAMultiCloudIntel — Web Application

A browser-based chat interface for the PESAMultiCloudIntel ICA Agent.
Select a cloud provider, ask natural language questions, and receive
AI-generated infrastructure insights powered by IBM Consulting Advantage.

---

## Architecture

```
Browser (localhost:5173)
    │  React 18 + TypeScript (Vite 5)
    │  CloudSelector | ChatWindow | ChatInput
    │
    │  POST /api/chat  ← proxied by Vite in development
    ▼
FastAPI Backend (localhost:8001)
    │  ICAAdapter — build_payload() + extract_response()
    │  Primary + 3 fallback extraction paths
    │
    │  POST https://langflow.servicesessentials.ibm.com/api/v1/run/<id>
    │  Authorization: Bearer <ICA_API_KEY>
    ▼
ICA Workflow API (IBM Consulting Advantage / Langflow)
    │
    ▼
ICA Agent  (15 tools: 8 MCP + 7 Context Studio)
    └── mcp_server.py  (port 8000, unchanged)
```

**Port summary — nothing conflicts:**

| Service | Port |
|---|---|
| React dev server (Vite) | 5173 |
| FastAPI backend | 8001 |
| MCP server (existing) | 8000 |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

---

### Step 1 — Install backend dependencies

```bash
cd webapp/backend
pip install -r requirements.txt
```

### Step 2 — Configure backend environment

```bash
cp webapp/backend/.env.example webapp/backend/.env
```

Open `webapp/backend/.env` and fill in your real values:

```env
ICA_WORKFLOW_URL=https://langflow.servicesessentials.ibm.com/api/v1/run/<your-workflow-id>
ICA_API_KEY=<your-ica-api-key>
```

Leave `BACKEND_PORT=8001` and `CORS_ORIGINS=*` as-is for local development.

### Step 3 — Start the backend

```bash
cd webapp/backend
uvicorn main:app --port 8001 --reload
```

Expected startup output:

```
INFO  ============================================================
INFO  PESAMultiCloudIntel Backend starting up
INFO    Port        : 8001
INFO    CORS origins: ['http://localhost:5173']
INFO  ============================================================
INFO  ICAAdapter initialised successfully.
```

Verify it is running:

```bash
curl http://localhost:8001/health
# {"status":"ok"}

curl http://localhost:8001/
# {"name":"PESAMultiCloudIntel Backend","version":"1.0.0",...}
```

### Step 4 — Install frontend dependencies

Open a **new terminal**:

```bash
cd webapp/frontend
npm install
```

### Step 5 — Start the frontend

```bash
cd webapp/frontend
npm run dev
```

Open your browser at **http://localhost:5173**

---

## Usage

1. Select a cloud provider pill: **All Clouds**, **AWS**, **Azure**, or **GCP**
2. Type a natural language question in the input box
3. Press **Send** or **Enter** — use **Shift+Enter** to insert a newline
4. The AI response appears in the chat window, rendered with Markdown formatting

### Example questions

| Cloud | Question |
|---|---|
| All Clouds | "Which resources are consuming the most budget this month?" |
| AWS | "Which EC2 instances have been idle for the past 2 weeks?" |
| Azure | "Show me the top 10 most expensive Azure resources" |
| GCP | "Are there any GCP cost anomalies in the last 30 days?" |
| All Clouds | "Check compliance for missing encryption tags across all clouds" |

---

## Backend API Reference

### `GET /`

Returns service metadata.

```json
{
  "name": "PESAMultiCloudIntel Backend",
  "version": "1.0.0",
  "description": "Proxy API for the ICA Workflow (IBM Consulting Advantage).",
  "endpoints": { "health": "GET /health", "chat": "POST /api/chat" }
}
```

### `GET /health`

```json
{ "status": "ok" }
```

### `POST /api/chat`

**Request body:**

```json
{
  "question": "Which instances are idle?",
  "cloud_provider": "aws"
}
```

- `question` — required, must not be empty
- `cloud_provider` — one of `all`, `aws`, `azure`, `gcp` (default: `all`)

**Success response (200):**

```json
{
  "answer": "Here are the idle AWS instances…",
  "cloud_provider": "aws"
}
```

**Error responses:**

| Status | Cause |
|---|---|
| 422 | Empty question or invalid cloud_provider value |
| 502 | ICA Workflow API returned a non-2xx response |
| 503 | Backend adapter not initialised (startup failure) |
| 500 | Unexpected server error |

---

## Cloud Provider Context Injection

Before each ICA API call the adapter appends a context sentence to the question:

| Selection | Appended text |
|---|---|
| All Clouds | "Analyze across AWS, Azure and GCP." |
| AWS | "Focus on Amazon Web Services only." |
| Azure | "Focus on Microsoft Azure only." |
| GCP | "Focus on Google Cloud Platform only." |

---

## Environment Variables

### Backend (`webapp/backend/.env`)

| Variable | Required | Default | Description |
|---|---|---|---|
| `ICA_WORKFLOW_URL` | ✅ | — | Full Langflow run URL |
| `ICA_API_KEY` | ✅ | — | Bearer token for ICA auth |
| `BACKEND_PORT` | ❌ | `8001` | Port shown in startup log |
| `CORS_ORIGINS` | ❌ | `http://localhost:5173` | Comma-separated allowed origins |

`CORS_ORIGINS` defaults to `http://localhost:5173` when the variable is absent.  
Setting `CORS_ORIGINS=*` permits all origins (development only).

---

## Development Notes

### Frontend proxy

In development Vite proxies all `/api/*` requests to `http://localhost:8001`.
The proxy is configured in [`vite.config.ts`](frontend/vite.config.ts).

In production, configure a reverse proxy (nginx, etc.) to route `/api/*` to the FastAPI backend.

### TypeScript

Run the type-checker without building:

```bash
cd webapp/frontend
npm run lint          # tsc --noEmit
```

### ICA response extraction

The adapter tries four paths in order, logging a `WARNING` for each failed attempt:

1. `outputs[0].outputs[0].results.message.text` ← primary
2. `outputs[0].outputs[0].messages[0].message`
3. `outputs[0].outputs[0].artifacts.message`
4. Raw JSON dump of full response (always succeeds)

---

## Project Structure

```
webapp/
├── README.md                      ← This file
├── backend/
│   ├── main.py                    ← FastAPI app (lifespan, CORS, /api/chat, /health)
│   ├── ica_adapter.py             ← ICA Workflow API adapter (payload + extraction)
│   ├── requirements.txt           ← fastapi, uvicorn, httpx, python-dotenv, pydantic
│   └── .env.example               ← Environment template (copy to .env)
└── frontend/
    ├── index.html                 ← Vite HTML entry point
    ├── package.json               ← React 18, Vite 5, TypeScript, axios, react-markdown
    ├── vite.config.ts             ← Dev proxy /api → http://localhost:8001
    ├── tsconfig.json              ← strict TypeScript config
    ├── tsconfig.node.json         ← TypeScript project ref for Vite config
    └── src/
        ├── main.tsx               ← React 18 createRoot entry point
        ├── App.tsx                ← Root component — owns all state
        ├── App.css                ← Shell layout + component styles
        ├── index.css              ← CSS reset + variables + base elements
        ├── types.ts               ← CloudProvider, Message, ChatRequest, ChatResponse
        ├── api/
        │   └── chat.ts            ← sendChat() — axios + typed error handling
        └── components/
            ├── CloudSelector.tsx  ← Provider pill buttons (brand colours)
            ├── ChatWindow.tsx     ← Scrollable messages + ReactMarkdown + dots loader
            └── ChatInput.tsx      ← Auto-resize textarea + Send button
```
