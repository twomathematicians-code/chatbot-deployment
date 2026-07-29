import pytest
from httpx import ASGITransport, AsyncClient
from src.api.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_chat(client):
    r = await client.post("/api/v1/chat", json={"message": "Hello, what can you help with?"})
    assert r.status_code == 200
    d = r.json()
    assert "reply" in d
    assert "intent" in d

@pytest.mark.asyncio
async def test_intent(client):
    r = await client.post("/api/v1/chat/intent?text=I%20want%20a%20refund")
    assert r.status_code == 200
    assert "top_intent" in r.json()

@pytest.mark.asyncio
async def test_qa(client):
    r = await client.post("/api/v1/chat/qa", json={
        "question": "What is the return policy?",
        "document_context": "Our return policy allows customers to return items within 30 days of purchase for a full refund."
    })
    assert r.status_code == 200
    d = r.json()
    assert len(d["relevant_excerpts"]) > 0

@pytest.mark.asyncio
async def test_telegram(client):
    r = await client.post("/api/v1/telegram/webhook", json={
        "update_id": 1, "message": {"text": "Hi", "from": {"id": 42}, "chat": {"id": 42}}
    })
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_whatsapp(client):
    r = await client.post("/api/v1/whatsapp/webhook", json={"From": "1234567890", "Body": "Hello"})
    assert r.status_code == 200
