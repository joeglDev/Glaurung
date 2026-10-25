from lib.prompts.utils.get_evaluator_prompt import get_evaluator_prompt
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

# If the number of completions in the chat loop exceeds MAXIMUM_ITERATIONS the chat is terminated to conserve resources.
MAXIMUM_ITERATIONS = 3


class ChatOrchestrator:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self._inference = OllamaWrapper(self._model_name)
        self._evaluator = OllamaWrapper("gemma4:e2b")
        self._messages = [OllamaMessage(role=OllamaRoles.SYSTEM, content=SYSTEM_PROMPT)]
        self._current_interation = 0
        self._passes_evaluation = False

    def _get_response(self) -> ClientChatResponse:
        message_id = f"{self._current_interation}-{uuid1()}"
        completion = self._inference.get_completion(messages=self._messages)
        msg_role = (
            ChatResponseRole.AGENT
            if completion.message.role == "assistant"
            else ChatResponseRole.TOOL
        )

        return ClientChatResponse(
            message=completion.message.content,
            role=msg_role,
            status=ChatResponseStatus.WORKING,
            id=message_id,
            reasoning=completion.message.thinking,
        )

    def _get_evaluation(self, initial_prompt: str, latest_completion: str | None):
        """Uses a small model to evaluate the latest message against the input prompt
        in order to determine if the prompt has been answered.
        """
        if latest_completion is None:
            return

        messages = [
            OllamaMessage(
                role=OllamaRoles.USER,
                content=get_evaluator_prompt(initial_prompt, latest_completion),
            )
        ]
        evaluation = self._evaluator.get_completion(messages=messages)

        if evaluation.message.content and "1" in evaluation.message.content:
            self._passes_evaluation = True
        else:
            evaluation_failed_message = (
                "The previous response did not answer the question. Try again."
            )
            self._messages.append(
                OllamaMessage(
                    role=OllamaRoles.ASSISTANT, content=evaluation_failed_message
                )
            )

    def _should_continue(self):
        if self._passes_evaluation:
            return False

        if self._current_interation == MAXIMUM_ITERATIONS:
            return False

        return True

    def chat(self, prompt: str) -> Iterator[ClientChatResponse]:
        self._messages.append(OllamaMessage(role=OllamaRoles.USER, content=prompt))

        # 1. Continue loop if response fails evaluation or iteration count < max
        while self._should_continue():
            self._current_interation += 1
            is_last_iteration = self._current_interation == MAXIMUM_ITERATIONS

            # 2. Get response and append to messages
            response = self._get_response()
            self._messages.append(
                OllamaMessage(
                    role=OllamaRoles.ASSISTANT, content=response.message or ""
                )
            )

            # 3. Evaluate if the response answers the initial prompt
            self._get_evaluation(
                initial_prompt=prompt, latest_completion=response.message
            )

            # 4. If the evaluation passes or loop runs to max iterations end the loop; otherwise continue
            if self._passes_evaluation or is_last_iteration:
                response.status = ChatResponseStatus.COMPLETE
                yield response
            else:
                yield response
