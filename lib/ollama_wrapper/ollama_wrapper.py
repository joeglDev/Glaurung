import ollama


class OllamaWrapper:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._check_model()

    def _check_model(self):
        try:
            available_models = ollama.list()
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

    def run(self):
        pass


# wrapper = OllamaWrapper("gemma4:e2b")
# wrapper.run()
