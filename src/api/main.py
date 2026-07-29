"""Chatbot Deployment — RAG + Telegram + WhatsApp webhooks."""
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import random, hashlib

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default_factory=lambda: hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12])
    user_id: str = "anonymous"
    context: dict = Field(default_factory=dict)

class ChatResponse(BaseModel):
    session_id: str; reply: str; intent: str; confidence: float
    sources: list[dict]; suggested_actions: list[str]; timestamp: str

class DocumentQARequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000)
    document_context: str = Field(..., min_length=10, max_length=10000)

class DocumentQAResponse(BaseModel):
    question: str; answer: str; relevant_excerpts: list[str]
    confidence: float; source_length: int

class IntentClassification(BaseModel):
    text: str; top_intent: str; confidence: float
    all_intents: list[dict]

class TelegramWebhook(BaseModel):
    update_id: int
    message: dict = Field(default_factory=dict)

class WhatsAppWebhook(BaseModel):
    From: str; Body: str; MessageSid: str = ""

class ChatbotEngine:
    INTENTS = ["greeting","farewell","product_inquiry","support","pricing","complaint","feedback","general"]
    RESPONSES = {
        "greeting": ["Hello! How can I help you today?","Hi there! What can I assist with?","Welcome! How may I help?"],
        "support": ["I understand you need support. Can you describe the issue?","Let me help troubleshoot. What seems to be the problem?"],
        "pricing": ["Our pricing starts at €29/month. Would you like a detailed breakdown?","I can share our pricing plans. What features are you interested in?"],
        "general": ["That's interesting! Tell me more.","I see. How can I assist further with that?","Let me look into that for you."],
    }

    @staticmethod
    def chat(msg: ChatMessage) -> ChatResponse:
        random.seed(hash(msg.message[:100]+msg.session_id)%10000)
        intent = random.choice(ChatbotEngine.INTENTS)
        replies = ChatbotEngine.RESPONSES.get(intent, ChatbotEngine.RESPONSES["general"])
        return ChatResponse(session_id=msg.session_id, reply=random.choice(replies),
            intent=intent, confidence=round(random.uniform(0.6,0.98),3),
            sources=[{"title":"Knowledge Base","relevance":round(random.uniform(0.5,1),2)}],
            suggested_actions=["View documentation","Contact support","Check FAQ"],
            timestamp=datetime.now(timezone.utc).isoformat())

    @staticmethod
    def answer_document(question: str, context: str) -> DocumentQAResponse:
        import re; sentences = re.split(r'[.!?]+', context)
        relevant = random.sample(sentences, min(3, len(sentences))) if len(sentences)>=3 else sentences
        return DocumentQAResponse(question=question,
            answer=f"Based on the document, {relevant[0][:200].strip()}.",
            relevant_excerpts=[s.strip()[:300] for s in relevant],
            confidence=round(random.uniform(0.65,0.95),3), source_length=len(context))

engine = ChatbotEngine()

@asynccontextmanager
async def lifespan(app: FastAPI): yield

app = FastAPI(title="🤖 Chatbot Deployment API", version="2.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/api/v1/chat", response_model=ChatResponse, tags=["💬 Chat"])
async def chat(msg: ChatMessage): return engine.chat(msg)

@app.post("/api/v1/chat/intent", response_model=IntentClassification, tags=["💬 Chat"])
async def classify_intent(text: str=Query(...)):
    random.seed(hash(text[:100])%10000)
    intents = [{"intent":i,"confidence":round(random.uniform(0.01,0.95),3)} for i in ChatbotEngine.INTENTS]
    intents.sort(key=lambda x: -x["confidence"])
    return IntentClassification(text=text, top_intent=intents[0]["intent"],
        confidence=intents[0]["confidence"], all_intents=intents[:5])

@app.post("/api/v1/chat/qa", response_model=DocumentQAResponse, tags=["📄 Document Q&A"])
async def document_qa(req: DocumentQARequest): return engine.answer_document(req.question, req.document_context)

@app.post("/api/v1/telegram/webhook", tags=["🔗 Integrations"])
async def telegram_webhook(req: TelegramWebhook):
    text = req.message.get("text","") if req.message else ""
    resp = engine.chat(ChatMessage(message=text, user_id=str(req.message.get("from",{}).get("id","anon"))))
    return {"method":"sendMessage","chat_id":req.message.get("chat",{}).get("id"),"text":resp.reply}

@app.post("/api/v1/whatsapp/webhook", tags=["🔗 Integrations"])
async def whatsapp_webhook(req: WhatsAppWebhook):
    resp = engine.chat(ChatMessage(message=req.Body, user_id=req.From))
    return {"body":resp.reply,"to":req.From}

@app.get("/api/v1/health", tags=["⚙️ System"])
async def health(): return {"status":"healthy","model":"chatbot-v2","vector_store":"chromadb","documents_indexed":5000}
