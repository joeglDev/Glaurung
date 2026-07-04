from google.protobuf.json_format import MessageToDict
from a2a.types import AgentInterface, AgentProvider, AgentCapabilities, AgentCard


class GlaurungAgentCard:
    def __init__(self):
        self._skills = []
        self._capabilities = AgentCapabilities(streaming=True)
        self._agent_provider = AgentProvider(url="https://github.com/joeglDev")
        self._supported_interfaces = [
            AgentInterface(
                url="http://127.0.0.1:8000/chat/stream",
                protocol_version="1.0",
                protocol_binding="HTTP+JSON",
            )
        ]
        self._card = AgentCard(
            name="Glaurung",
            description="A self-made minimal Ai agent using local inference.",
            supported_interfaces=self._supported_interfaces,
            provider=self._agent_provider,
            version="0.1.0",
            capabilities=self._capabilities,
            default_input_modes=["string chat"],
            skills=self._skills,
            # TODO: commission an artist for the iconUrl
        )

    def get_agent_card(self):
        return MessageToDict(self._card, preserving_proto_field_name=True)
