from models.chat.ollama_roles import OllamaRoles
from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: OllamaRoles
    content: str
