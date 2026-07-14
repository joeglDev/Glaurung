from enum import StrEnum
from pydantic import BaseModel


class ChatResponseStatus(StrEnum):
    COMPLETE = "COMPLETE"
    PENDING = "PENDING"
    THINKING = "THINKING"
    WORKING = "WORKING"


class ChatResponseRole(StrEnum):
    AGENT = "AGENT"
    TOOL = "TOOL"


class ClientChatResponse(BaseModel):
    role: str
    status: str
    message: str | None
    id: str
