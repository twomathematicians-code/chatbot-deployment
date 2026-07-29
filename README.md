<div align="center">

# Chatbot Deployment Platform

### RAG + Multi-Turn + Telegram + WhatsApp + Intent Classification

[![FastAPI](https://img.shields.io/badge/FastAPI-Webhooks-009688)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector-Store-E040FB)](https://chromadb.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docker.com)

</div>

---

## Architecture

```
Telegram + WhatsApp + REST --> FastAPI Router --> Intent Classifier --> Response Generator
                                                        |
                                                   ChromaDB Vector Store
```


## Features

- **RAG Document Q&A** -- upload docs, ask questions, get sourced answers
- **Intent Classification** -- 8 intents with confidence scoring
- **Multi-channel** -- Telegram + WhatsApp webhook connectors
- **Session Management** -- per-session context tracking

## Run

```bash
docker compose up -d

curl -X POST http://localhost:8000/api/v1/chat -d '{"message": "What products do you have?", "session_id": "sess-1"}'
curl -X POST http://localhost:8000/api/v1/chat/qa -d '{"question": "What is the refund policy?", "document_context": "Our refund policy allows returns within 30 days..."}'
```


## Endpoints

- `POST /api/v1/chat` -- Conversational response
- `POST /api/v1/chat/intent` -- Classify intent
- `POST /api/v1/chat/qa` -- Document Q&A
- `POST /api/v1/telegram/webhook` -- Telegram bot
- `POST /api/v1/whatsapp/webhook` -- WhatsApp bot

---

<p align="center"><i>Mahesh Solanki</i> -- <a href="https://github.com/twomathematicians-code">GitHub</a></p>
