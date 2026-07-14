from lib.utils.get_message_status import get_message_status
from typing import AsyncIterable
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

    async def _get_response(self) -> AsyncIterable[ClientChatResponse]:
        full_completion = ""
        stream = self._inference.get_completion(messages=self._messages)

        async for chunk in stream:
            message_id = f"{uuid1()}"  # todo add message number here

            if chunk.message.content:
                full_completion += chunk.message.content

            if chunk.done:
                self._messages.append(
                    OllamaMessage(role=OllamaRoles.ASSISTANT, content=full_completion)
                )

                yield ClientChatResponse(
                    message=full_completion,
                    role=ChatResponseRole.AGENT,
                    status=ChatResponseStatus.COMPLETE,
                    id=message_id,
                )

            if not chunk.done:
                role = (
                    ChatResponseRole.AGENT
                    if chunk.message.role == "assistant"
                    else ChatResponseRole.TOOL
                )
                status = get_message_status(chunk.message)

                response = ClientChatResponse(
                    message=chunk.message.content,
                    role=role,
                    status=status,
                    id=message_id,
                )
                yield response

    async def chat(self, prompt: str) -> AsyncIterable[ClientChatResponse]:
        self._messages.append(OllamaMessage(role=OllamaRoles.USER, content=prompt))
        stream = self._get_response()

        async for msg in stream:
            yield msg
