from models.responses.client_chat_response import ClientChatResponse
from lib.chat_orchestrator.chat_orchestrator import ChatOrchestrator
from models.requests.chat_stream_request import ChatStreamRequest
from lib.card.glaurung_agent_card import GlaurungAgentCard
from typing import AsyncIterable

from fastapi import FastAPI

app = FastAPI()
chat = ChatOrchestrator("gemma4:e2b")


@app.get("/")
def ping() -> str:
    return "pong"


@app.get("/.well-known/agent-card.json")
def fetch_agent_card():
    agent_card = GlaurungAgentCard()
    return agent_card.get_agent_card()


@app.post("/chat/stream")
async def get_chat_completion(
    req: ChatStreamRequest,
) -> AsyncIterable[ClientChatResponse]:
    try:
        for response in chat.chat(req.prompt):
            yield response
    except Exception as e:
        print(e)  # TODO: In production log e and sanitise errors returns for users
