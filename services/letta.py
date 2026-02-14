from letta_client import AsyncLetta, APIError
from config.settings import settings
from utils.logger import setup_logger
from typing import Optional

logger = setup_logger(__name__)


class LettaService:
    """Service for interacting with Letta API"""

    def __init__(self):
        self.client = AsyncLetta(
            api_key=settings.letta_api_key,
            base_url=settings.letta_base_url,
        )
        self.agent_id = settings.letta_agent_id

    async def create_conversation(self) -> Optional[str]:
        """
        Create a new conversation for the agent.

        Returns:
            Conversation ID or None if failed
        """
        try:
            conversation = await self.client.conversations.create(
                agent_id=self.agent_id
            )
            logger.info(f"Created Letta conversation: {conversation.id}")
            return conversation.id
        except APIError as e:
            logger.error(f"Failed to create Letta conversation: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating Letta conversation: {e}")
            return None

    async def send_message(
        self, conversation_id: str, message: str
    ) -> Optional[str]:
        """
        Send a message to a Letta conversation and extract response text.

        Args:
            conversation_id: Letta conversation ID
            message: User message content

        Returns:
            Assistant response text or None if failed
        """
        try:
            # Send message to conversation (non-streaming)
            response = await self.client.conversations.messages.create(
                conversation_id=conversation_id,
                messages=[{"role": "user", "content": message}],
                streaming=False,
            )

            logger.info(f"Letta response type: {type(response)}")

            # Extract assistant message content
            response_text = self._extract_response_text(response)
            return response_text

        except APIError as e:
            logger.error(f"Letta API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error sending message to Letta: {e}")
            return None

    def _extract_response_text(self, response) -> Optional[str]:
        """
        Extract assistant message text from Letta response.

        Args:
            response: Letta API response

        Returns:
            Assistant message content or None if not found
        """
        try:
            logger.info(f"Letta response type: {type(response)}")
            logger.info(f"Letta response attributes: {dir(response)}")

            # Response contains messages array with different types
            if hasattr(response, "messages") and response.messages:
                logger.info(f"Response has {len(response.messages)} messages")
                for i, message in enumerate(response.messages):
                    logger.info(f"Message {i}: type={type(message)}, attrs={dir(message)}")
                    # Check for assistant_message type
                    if hasattr(message, "message_type"):
                        logger.info(f"Message {i} message_type: {message.message_type}")
                        if message.message_type == "assistant_message":
                            if hasattr(message, "content") and message.content:
                                logger.info(f"Found assistant message: {message.content}")
                                return message.content

            # Fallback: try to get content directly
            if hasattr(response, "content"):
                logger.info(f"Using fallback content: {response.content}")
                return response.content

            logger.warning("No assistant message found in Letta response")
            return None

        except Exception as e:
            logger.error(f"Error extracting response text: {e}")
            return None


letta_service = LettaService()
