from base.api_client import APIClient
from config.settings import settings
from utils.logger import setup_logger
from typing import Optional

logger = setup_logger(__name__)


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

    async def create_conversation(self) -> Optional[str]:
        """
        Create a new conversation for the agent.

        Returns:
            Conversation ID or None if failed
        """
        try:
            response = await self.client.post(
                "/v1/conversations",
                params={"agent_id": self.agent_id},
            )
            conversation_id = response.get("id")
            logger.info(f"Created Letta conversation: {conversation_id}")
            return conversation_id
        except Exception as e:
            logger.error(
                f"Failed to create Letta conversation: {type(e).__name__}: {e}"
            )
            return None

    async def send_message(self, conversation_id: str, message: str) -> Optional[str]:
        """
        Send a message to a Letta conversation and extract response text.

        Args:
            conversation_id: Letta conversation ID
            message: User message content

        Returns:
            Assistant response text or None if failed
        """
        try:
            response = await self.client.post(
                f"/v1/conversations/{conversation_id}/messages",
                data={
                    "messages": [{"role": "user", "content": message}],
                    "streaming": False,
                },
            )

            response_text = self._extract_response_text(response)
            return response_text

        except Exception as e:
            logger.error(f"Failed to send message to Letta: {type(e).__name__}: {e}")
            return None

    def _extract_response_text(self, data: dict) -> Optional[str]:
        """
        Extract assistant message text from Letta response JSON.

        Args:
            data: Parsed JSON response from Letta API

        Returns:
            Assistant message content or None if not found
        """
        try:
            messages = data.get("messages", [])
            for message in messages:
                if message.get("message_type") == "assistant_message":
                    content = message.get("content")
                    if content:
                        logger.info(f"Extracted assistant message: {content[:100]}...")
                        return content

            logger.warning("No assistant message found in Letta response")
            return None

        except Exception as e:
            logger.error(f"Error extracting response text: {e}")
            return None


letta_service = LettaService()
