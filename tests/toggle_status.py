import asyncio
import json
from utils.logger import setup_logger
from config.settings import settings
from base.api_client import APIClient
from base.models import ConversationStatus
from pydantic import BaseModel


class Account(BaseModel):
    account_id: int
    conversation_id: int


logger = setup_logger(__name__)

client = APIClient(
    base_url=settings.chatwoot_base_url,
    api_key=settings.chatwoot_user_api_key,
    auth_header_name="api_access_token",
    auth_header_prefix=None,
)


async def get_conversation_status(account_id: int, conversation_id: int):
    # get {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}
    endpoint = f"/api/v1/accounts/{account_id}/conversations/{conversation_id}"
    response = await client.get(endpoint)
    status = response.get("status")
    logger.info(f"Status: {status}")
    return status


async def toggle_status(
    account_id: int, conversation_id: int, status: ConversationStatus
):
    logger.info(
        f"toggling status of conversation {conversation_id} in account {account_id}"
    )
    # {base_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status
    endpoint = (
        f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status"
    )
    response = await client.post(endpoint, data=status.model_dump())
    logger.info(f"Response: {json.dumps(response, indent=2)}")


async def main():

    account = Account(account_id=1, conversation_id=3)
    # get current status of conversation
    status = await get_conversation_status(account.account_id, account.conversation_id)
    if status == "open":
        status = ConversationStatus(status="resolved", snoozed_until=None)
        logger.info("Status changed to resolved")
    else:
        status = ConversationStatus(status="open", snoozed_until=None)
        logger.info("Status changed to open")

    await toggle_status(account.account_id, account.conversation_id, status)


if __name__ == "__main__":
    asyncio.run(main())
