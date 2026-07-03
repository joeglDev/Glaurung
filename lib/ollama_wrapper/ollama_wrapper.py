from typing import AsyncIterable
from lib.ollama_wrapper.SYSTEM_PROMPT import SYSTEM_PROMPT
from ollama import list, ChatResponse, AsyncClient


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

    async def get_completion(self, prompt: str) -> AsyncIterable[ChatResponse]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]

        async for chunk in await AsyncClient().chat(  # noqa: F821
            model=self.model_name, messages=messages, stream=True
        ):
            yield chunk


"""
wrapper = OllamaWrapper("gemma4:e2b")

async def main(
):
    stream = wrapper.get_completion(prompt="say hello")
    async for chunk in stream:
        print(chunk.message.content)

asyncio.run(main())
"""
