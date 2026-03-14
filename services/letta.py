from base.api_client import APIClient
from config.settings import settings
from utils.logger import setup_logger
from typing import Optional, Any

logger = setup_logger(__name__)

# Tool source code for send_chatwoot_message (client-side execution)
CHATWOOT_TOOL_SOURCE = '''
def send_chatwoot_message(
    content: str,
    content_type: str = "text",
    content_attributes: dict = None
) -> str:
    """
    Send a message to the Chatwoot conversation.

    Use this tool to reply to the customer. Supports interactive messages.

    Args:
        content: Message content or description
        content_type: Message type - "text", "input_select", "form", "cards", "article"
        content_attributes: Additional attributes for interactive messages (items, actions, etc.)

    Returns:
        Confirmation or error message

    Examples:
        # Simple text
        send_chatwoot_message("Hello! How can I help?")

        # Options menu
        send_chatwoot_message("Select an option:", "input_select", {
            "items": [{"title": "Sales", "value": "sales"}, {"title": "Support", "value": "support"}]
        })
    """
    # This tool executes client-side only
    raise Exception("Client-side execution required")
'''


class LettaService:
    """Service for interacting with Letta API via direct HTTP calls."""

    def __init__(self):
        self.client = APIClient(
            base_url=settings.letta_base_url,
            api_key=settings.letta_api_key,
            auth_header_name="Authorization",
            auth_header_prefix="Bearer",
            timeout=60.0,  # Letta API can be slow
        )
        self.agent_id = settings.letta_agent_id

    async def create_chatwoot_tool(self) -> Optional[str]:
        """
        Create the send_chatwoot_message tool for client-side execution.

        Returns:
            Tool ID or None if failed
        """
        try:
            response = await self.client.post(
                "/v1/tools",
                data={
                    "source_code": CHATWOOT_TOOL_SOURCE,
                    "default_requires_approval": True,  # Client-side execution
                },
            )
            tool_id = response.get("id")
            logger.info(f"Created Chatwoot tool: {tool_id}")
            return tool_id
        except Exception as e:
            logger.error(f"Failed to create Chatwoot tool: {type(e).__name__}: {e}")
            return None

    async def create_agent(self, name: str = None) -> Optional[str]:
        """
        Create a new Letta agent using settings.

        Args:
            name: Optional agent name

        Returns:
            Agent ID or None if failed
        """
        try:
            # Create the Chatwoot tool first
            tool_id = await self.create_chatwoot_tool()
            if not tool_id:
                logger.error("Failed to create Chatwoot tool, aborting agent creation")
                return None

            response = await self.client.post(
                "/v1/agents",
                data={
                    "name": name or "chatwoot-agent",
                    "model": settings.letta_model,
                    "embedding": settings.letta_embedding,
                    "memory_blocks": [
                        {"label": "persona", "value": settings.letta_agent_persona},
                        {
                            "label": "human",
                            "value": "Customer information will be stored here.",
                        },
                    ],
                    "tool_ids": [tool_id],
                    "include_base_tools": True,  # archival_memory tools
                },
            )
            agent_id = response.get("id")
            logger.info(f"Created Letta agent: {agent_id}")
            return agent_id
        except Exception as e:
            logger.error(f"Failed to create Letta agent: {type(e).__name__}: {e}")
            return None

    async def create_conversation(self, agent_id: str = None) -> Optional[str]:
        """
        Create a new conversation for the agent.

        Args:
            agent_id: Optional agent ID (uses default if not provided)

        Returns:
            Conversation ID or None if failed
        """
        target_agent_id = agent_id or self.agent_id
        try:
            response = await self.client.post(
                "/v1/conversations",
                params={"agent_id": target_agent_id},
            )
            conversation_id = response.get("id")
            logger.info(f"Created Letta conversation: {conversation_id}")
            return conversation_id
        except Exception as e:
            logger.error(
                f"Failed to create Letta conversation: {type(e).__name__}: {e}"
            )
            return None

    async def send_message(self, conversation_id: str, message: str) -> Optional[dict]:
        """
        Send a message to a Letta conversation.

        Args:
            conversation_id: Letta conversation ID
            message: User message content

        Returns:
            Full response dict (contains messages array with potential approval_request_message)
        """
        try:
            response = await self.client.post(
                f"/v1/conversations/{conversation_id}/messages",
                data={
                    "messages": [{"role": "user", "content": message}],
                    "streaming": False,
                },
            )
            return response
        except Exception as e:
            logger.error(f"Failed to send message to Letta: {type(e).__name__}: {e}")
            return None

    async def send_tool_result(
        self,
        conversation_id: str,
        tool_call_id: str,
        result: str,
        status: str = "success",
    ) -> Optional[dict]:
        """
        Send tool execution result back to the agent.

        Args:
            conversation_id: Letta conversation ID
            tool_call_id: ID of the tool call
            result: Tool execution result
            status: "success" or "error"

        Returns:
            Agent response after receiving tool result
        """
        try:
            response = await self.client.post(
                f"/v1/conversations/{conversation_id}/messages",
                data={
                    "messages": [
                        {
                            "type": "approval",
                            "approvals": [
                                {
                                    "type": "tool",
                                    "tool_call_id": tool_call_id,
                                    "tool_return": result,
                                    "status": status,
                                }
                            ],
                        }
                    ],
                },
            )
            logger.info(f"Sent tool result for tool_call_id: {tool_call_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to send tool result: {type(e).__name__}: {e}")
            return None


letta_service = LettaService()
