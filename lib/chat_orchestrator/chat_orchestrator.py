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
MAXIMUM_ITERATIONS = 2


class ChatOrchestrator:
    def __init__(self, model_name: str):
        self._model_name = model_name
        self._inference = OllamaWrapper(self._model_name)
        self._messages = [OllamaMessage(role=OllamaRoles.SYSTEM, content=SYSTEM_PROMPT)]
        self.current_interation = 0

    def _get_response(self) -> ClientChatResponse:
        message_id = f"{self.current_interation}-{uuid1()}"
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

    """
TODO: Evaluate the response and terminate the while loop if response is adequate.


    """

    def chat(self, prompt: str) -> Iterator[ClientChatResponse]:
        self._messages.append(OllamaMessage(role=OllamaRoles.USER, content=prompt))

        while self.current_interation < MAXIMUM_ITERATIONS:
            self.current_interation += 1
            is_last_iteration = self.current_interation == MAXIMUM_ITERATIONS

            if is_last_iteration:
                response = self._get_response()
                response.status = ChatResponseStatus.COMPLETE
                yield response
            else:
                yield self._get_response()
