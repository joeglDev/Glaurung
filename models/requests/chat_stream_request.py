from pydantic import BaseModel


class ChatStreamRequest(BaseModel):
    prompt: str
