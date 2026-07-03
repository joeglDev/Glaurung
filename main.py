from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from lib.ollama_wrapper.ollama_wrapper import OllamaWrapper

app = FastAPI()


@app.get("/")
def ping():
    return "pong"


@app.post("/chat/stream", response_class=StreamingResponse)
async def get_chat_completion(prompt: str) -> AsyncGenerator[str | None]:
    wrapper = OllamaWrapper("gemma4:e2b")
    stream = wrapper.get_completion(prompt=prompt)
    async for chunk in stream:
        yield chunk.message.content
