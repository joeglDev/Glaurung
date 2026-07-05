from dataclasses import asdict
from models.chat.ollama_roles import OllamaRoles
from models.chat.chat_message import ChatMessage
from uuid import uuid1
from typing import AsyncIterable
from lib.prompts.SYSTEM_PROMPT import SYSTEM_PROMPT
from ollama import list, ChatResponse, AsyncClient

from models.responses.client_chat_response import ClientChatResponse


class OllamaWrapper:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._check_model()
        self._messages = [ChatMessage(role=OllamaRoles.SYSTEM, content=SYSTEM_PROMPT)]

    def _check_model(self):
        try:
            available_models = list()
            models_count = len(available_models.models)
            model_names = [x.model.strip() for x in available_models.models if x.model]

            if models_count == 0:
                raise Exception(
                    "No models are available. Please use ollama to install a local model."
                )
            else:
                print(f"There are {models_count} models available:")
                print(model_names)

                if all(self.model_name.strip() != x for x in model_names):
                    raise Exception(
                        f"Model {self.model_name} not available. Please download this model to ollama first."
                    )

        except Exception as e:
            raise e

    async def _get_completion(self, prompt: str) -> AsyncIterable[ChatResponse]:
        self._messages.append(ChatMessage(role=OllamaRoles.USER, content=prompt))

        # todo return a2a compliant dict
        async for chunk in await AsyncClient().chat(
            model=self.model_name,
            messages=[asdict(message) for message in self._messages],
            stream=True,
        ):
            yield chunk

    async def get_response(self, prompt: str) -> AsyncIterable[ClientChatResponse]:
        full_completion = ""
        stream = self._get_completion(prompt=prompt)

        async for chunk in stream:
            message_id = f"{uuid1()}"  # todo add message number here

            if chunk.message.content:
                full_completion += chunk.message.content

            if chunk.done:
                self._messages.append(
                    ChatMessage(role=OllamaRoles.ASSISTANT, content=full_completion)
                )

                yield ClientChatResponse(
                    message=full_completion,
                    role="AGENT",
                    status="COMPLETE",
                    id=message_id,
                )

            if not chunk.done:
                role = "AGENT" if chunk.message.role == "assistant" else "TOOL"
                status = "WORKING"

                response = ClientChatResponse(
                    message=chunk.message.content,
                    role=role,
                    status=status,
                    id=message_id,
                )
                yield response
