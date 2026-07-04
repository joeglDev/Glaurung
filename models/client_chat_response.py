from pydantic import BaseModel


class ClientChatResponse(BaseModel):
    role: str  # TODO: use A2A role
    status: str  # TODO: use A2A status
    message: str | None
    id: str
