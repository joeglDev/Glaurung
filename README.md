# Glaurung

## Summary

An attempt to create a minimal agentic system using local inference.

## Quickstart

This agent uses [Ollama](https://ollama.com/) to provide local inference. Please ensure that Ollama is downloaded and running.

1. Run `uv sync` to install dependencies.
2. Start the server with `uv run fastapi dev`.

A simple curl request to test the system might be:
```bash
curl -X POST "http://127.0.0.1:8000/chat/stream" \
-H "Content-Type: application/json" \
-d "{\"prompt\": \"What are you?\"}"
```

## A2A

This project attempts to be compliant with the Agent2Agent (A2A) protocol.

- An agent card is available at the endpoint `/.well-known/agent-card.json`.

## Thats an interesting name

Yes, this system is named after Glaurung from JRR Tolkien's The Silmarillion. Glaurung is powerful but evil and manipulative.
I choose this name to highlight that genAI although powerful when used correctly is extremely easy to misuse leading to negative consequences.
