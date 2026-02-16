"""Test creating a Letta conversation (using direct httpx)."""
import asyncio
from services.letta import letta_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def test_create_conversation():
    """Test creating a Letta conversation."""
    logger.info("Starting Letta conversation creation test...")
    conversation_id = await letta_service.create_conversation()

    if conversation_id:
        logger.info(f"SUCCESS: Created conversation with ID: {conversation_id}")
    else:
        logger.info("FAILED: Could not create conversation")

    return conversation_id


if __name__ == "__main__":
    asyncio.run(test_create_conversation())
