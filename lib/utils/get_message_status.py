from ollama import Message

from models.responses.client_chat_response import ChatResponseStatus


def get_message_status(message: Message) -> str:
    if message.content and not message.thinking:
        return ChatResponseStatus.WORKING
    elif not message.content and message.thinking:
        return ChatResponseStatus.THINKING
    else:
        return ChatResponseStatus.PENDING
