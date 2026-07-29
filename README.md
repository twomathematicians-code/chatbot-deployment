# 🤖 ML Chatbot Deployment

[![CI/CD](https://github.com/twomathematicians-code/ml-chatbot-deployment/actions/workflows/ci.yml/badge.svg)](https://github.com/twomathematicians-code/ml-chatbot-deployment/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://hub.docker.com/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?logo=langchain)](https://www.langchain.com/)

**Production chatbot deployment platform: RAG-based conversational AI, multi-turn dialogue, Telegram & WhatsApp bot connectors, intent classification, and document Q&A — all containerized and CI/CD-ready.**

## 🎯 Chatbot Modules

| Module | Technology | Capability |
|---|---|---|
| **RAG Chatbot** | LangChain + ChromaDB | Document-grounded answers |
| **Intent Classifier** | DistilBERT Fine-tuned | Multi-class intent routing |
| **Multi-turn Dialogue** | ConversationBufferMemory | Context-aware responses |
| **Telegram Bot** | python-telegram-bot | Full Telegram integration |
| **WhatsApp Bot** | Twilio API | WhatsApp messaging |

## 🚀 Quick Start

```bash
git clone https://github.com/twomathematicians-code/ml-chatbot-deployment.git
cd ml-chatbot-deployment
docker-compose up --build
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/chat` | RAG-grounded chat |
| `POST` | `/api/v1/chat/intent` | Intent classification |
| `POST` | `/api/v1/chat/qa` | Document Q&A |
| `POST` | `/api/v1/telegram/webhook` | Telegram webhook |
| `POST` | `/api/v1/whatsapp/webhook` | WhatsApp webhook |
| `GET` | `/api/v1/health` | Health check |

## 👤 Author

**Mahesh Solanki** — [LinkedIn](https://linkedin.com/in/maheshsolanki-16b9a6a5) | [GitHub](https://github.com/twomathematicians-code)
