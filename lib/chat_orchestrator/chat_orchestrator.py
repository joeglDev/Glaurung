from typing import Iterator
from uuid import uuid1

from lib.ollama_wrapper.ollama_wrapper import OllamaWrapper
from lib.prompts.SYSTEM_PROMPT import SYSTEM_PROMPT
from models.chat.ollama_message import OllamaMessage
from models.chat.ollama_roles import OllamaRoles
from models.responses.client_chat_response import (
    ClientChatResponse,
    ChatResponseStatus,
    ChatResponseRole,
)


class ChatOrchestrator:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self._inference = OllamaWrapper(self._model_name)
        self._messages = [OllamaMessage(role=OllamaRoles.SYSTEM, content=SYSTEM_PROMPT)]
        self.current_interation = 0

    def _get_response(self) -> ClientChatResponse:
        message_id = f"{self.current_interation}-{uuid1()}"
        completion = self._inference.get_completion(messages=self._messages)
        print(f"role: {completion.message.role}")
        print(f"thinking: {completion.message.thinking}")

        return ClientChatResponse(
            message=completion.message.content,
            role=ChatResponseRole.AGENT,
            status=ChatResponseStatus.COMPLETE,
            id=message_id,
        )

    def chat(self, prompt: str) -> Iterator[ClientChatResponse]:
        self._messages.append(OllamaMessage(role=OllamaRoles.USER, content=prompt))

        while self.current_interation < 2:
            self.current_interation += 1
            yield self._get_response()
