from lib.card.glaurung_agent_card import GlaurungAgentCard
from typing import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from lib.ollama_wrapper.ollama_wrapper import OllamaWrapper

app = FastAPI()


@app.get("/")
def ping() -> str:
    return "pong"


@app.get("/.well-known/agent-card.json")
def fetch_agent_card():
    agent_card = GlaurungAgentCard()
    return agent_card.get_agent_card()


@app.post("/chat/stream", response_class=StreamingResponse)
async def get_chat_completion(prompt: str) -> AsyncIterable[str]:
    wrapper = OllamaWrapper("gemma4:e2b")
    async for chunk in wrapper.get_response(prompt):
        yield chunk.model_dump_json() + "\n"
