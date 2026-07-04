from uuid import uuid1
from typing import AsyncIterable
from lib.ollama_wrapper.SYSTEM_PROMPT import SYSTEM_PROMPT
from ollama import list, ChatResponse, AsyncClient

from models.client_chat_response import ClientChatResponse


class OllamaWrapper:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._check_model()

    def _check_model(self):
        try:
            available_models = list()
            models_count = len(available_models.models)

            print(f"There are {models_count} models available:")

            if models_count == 0:
                raise Exception(
                    "No models are available. Please use ollama to install a local model."
                )
            else:
                for model in available_models.models:
                    print(model.model)
        except Exception as e:
            print(e)
            raise e

    async def _get_completion(self, prompt: str) -> AsyncIterable[ChatResponse]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},  # todo: use python dataclass
            {"role": "user", "content": prompt},
        ]

        # todo return a2a compliant dict
        async for chunk in await AsyncClient().chat(
            model=self.model_name, messages=messages, stream=True
        ):
            yield chunk

    async def get_response(self, prompt: str) -> AsyncIterable[ClientChatResponse]:
        stream = self._get_completion(prompt=prompt)
        async for chunk in stream:
            role = "AGENT" if chunk.message.role == "assistant" else "TOOL"
            status = "WORKING"
            message_id = f"{uuid1()}"  # todo add message number here

            response = ClientChatResponse(
                message=chunk.message.content, role=role, status=status, id=message_id
            )
            yield response
