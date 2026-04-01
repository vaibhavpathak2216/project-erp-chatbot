# ERP Chatbot — Oracle Fusion Mock API Agent

A production-grade AI chatbot that interfaces with mock Oracle Fusion REST APIs using natural language. Powered by **Groq LLM** with **function calling**, served via **FastAPI**.

## Features

- 🤖 **LLM Function Calling** — Agent decides which API to call based on your query
- 📦 **Oracle Fusion-style APIs** — Purchase Orders, Suppliers, Inventory, HR, Invoices, Shipments
- ⚡ **FastAPI** — async, OpenAPI docs at `/docs`
- 🎨 **Built-in Chat UI** — served at `/` with quick query sidebar
- 🚀 **Render-ready** — one-click deploy with `render.yaml`

## Architecture

```
User message
    │
    ▼
FastAPI /chat endpoint
    │
    ▼
Groq LLM (function calling)
    │ decides which fn to call
    ▼
Mock Oracle API (chatbot_service.py)
    │ returns JSON data
    ▼
LLM formats natural language response
    │
    ▼
Chat UI renders answer (with table if structured)
```

## Local Development

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/project-erp-chatbot.git
cd project-erp-chatbot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variable
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Run
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 for the chat UI.  
Open http://127.0.0.1:8000/docs for the Swagger API explorer.

## API Reference

### `POST /chat`

```json
{
  "message": "Show me all open purchase orders",
  "conversation_history": []
}
```

**Response:**
```json
{
  "answer": "Here are the open purchase orders:\n\n**PO-2024-001**: ...",
  "function_called": "get_purchase_orders",
  "raw_data_fetched": true
}
```

## Pushing to GitHub

```bash
git init
git add .
git commit -m "feat: ERP chatbot with chat UI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/project-erp-chatbot.git
git push -u origin main
```

## Deploying on Render

1. Push your code to GitHub (above)
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — just click **Create Web Service**
5. Add your `GROQ_API_KEY` under **Environment → Environment Variables**
6. Wait ~2 min for build → your app is live at `https://erp-chatbot.onrender.com`

> **Free tier note:** Render's free plan spins down after 15 min of inactivity. First request may take ~30s to cold-start.

## Project Structure

```
project-erp-chatbot/
├── main.py                  # FastAPI app + UI serving
├── render.yaml              # Render deployment config
├── requirements.txt
├── .env                     # GROQ_API_KEY (not committed)
├── .gitignore
├── static/
│   └── index.html           # Chat UI
└── app/
    ├── __init__.py
    ├── chatbot_service.py   # LLM + function calling logic
    └── mock_oracle_api.py   # Mock Oracle Fusion endpoints
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq (llama3 / mixtral) |
| Backend | FastAPI + Uvicorn |
| Function Calling | Groq tool_use |
| Mock APIs | Python in-memory data |
| Frontend | Vanilla HTML/CSS/JS |
| Deploy | Render.com |
