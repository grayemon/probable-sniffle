import asyncio
import json
from config.settings import settings
from base.api_client import APIClient
from utils.logger import setup_logger

logger = setup_logger()

logger.info("Setting up chatwoot client")
logger.info(f"Chatwoot base URL: {settings.chatwoot_base_url}")
logger.info(f"Chatwoot agent bot API key: {settings.chatwoot_agent_bot_api_key}")

client = APIClient(
    base_url=settings.chatwoot_base_url,
    api_key=settings.chatwoot_agent_bot_api_key,
    auth_header_name="api_access_token",
    auth_header_prefix=None,
)

account_id = 1
conversation_id = 3
message = {"content": "hello"}


async def main():
    logger.info(
        f"sending message to conversation {conversation_id} in account {account_id}"
    )
    # {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages
    endpoint = f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
    response = await client.post(endpoint, data=message)
    logger.info(f"Response: {json.dumps(response, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
