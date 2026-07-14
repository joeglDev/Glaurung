from models.chat.ollama_roles import OllamaRoles
from dataclasses import dataclass


@dataclass
class OllamaMessage:
    role: OllamaRoles
    content: str
