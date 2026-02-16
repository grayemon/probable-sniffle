"""Test the LettaService class (using direct httpx)."""

import asyncio
from services.letta import letta_service
from utils.logger import setup_logger

logger = setup_logger(__name__)

conversation_id = "conv-0375ecef-c041-431a-a142-ed5fbffe383e"


async def test_service():
    """Test the LettaService.send_message method."""
    logger.info("=" * 50)
    logger.info("Testing LettaService.send_message...")

    response = await letta_service.send_message(
        conversation_id=conversation_id, message="Hello from the direct httpx test!"
    )

    if response:
        logger.info(f"SUCCESS! Response: {response}")
    else:
        logger.error("FAILED! No response received")


if __name__ == "__main__":
    asyncio.run(test_service())
