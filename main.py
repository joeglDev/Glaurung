from typing import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from lib.ollama_wrapper.ollama_wrapper import OllamaWrapper

app = FastAPI()


@app.get("/")
def ping():
    return "pong"


@app.post("/chat/stream", response_class=StreamingResponse)
async def get_chat_completion(prompt: str) -> AsyncIterable[str]:
    wrapper = OllamaWrapper("gemma4:e2b")
    async for chunk in wrapper.get_response(prompt):
        yield chunk.model_dump_json() + "\n"
