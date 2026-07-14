from dataclasses import asdict
from models.chat.ollama_message import OllamaMessage
from typing import AsyncIterable, List
from ollama import list as ollama_list, ChatResponse, AsyncClient


class OllamaWrapper:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._check_model()

    def _check_model(self):
        try:
            available_models = ollama_list()
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

    async def get_completion(
        self, messages: List[OllamaMessage]
    ) -> AsyncIterable[ChatResponse]:
        messages_as_dict = [asdict(message) for message in messages]

        async for chunk in await AsyncClient().chat(
            model=self.model_name,
            messages=messages_as_dict,
            stream=True,
        ):
            yield chunk
