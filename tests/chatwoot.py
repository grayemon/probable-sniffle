import asyncio
from services.chatwoot import chatwoot_service
from base.models import (
    ConversationParams,
    ConversationStatus,
    ConversationPriority,
    ConversationCustomAttributes,
)


async def main():
    params = ConversationParams(
        account_id=1,
        conversation_id=6,
        # status=ConversationStatus(status="open"),
        # priority=ConversationPriority(priority="low"),
        # custom_attributes=ConversationCustomAttributes(
        #    custom_attributes={
        #        "alternate_email": "[EMAIL_ADDRESS]",
        #        "letta_conversation_id": "1234567890"
        #    }
        # )
    )
    await chatwoot_service.send_message(params, "Hello from agent bot")
    # await chatwoot_service.get_messages(params)
    # await chatwoot_service.toggle_status(params)
    # await chatwoot_service.toggle_priority(params)
    # await chatwoot_service.get_conversation_details(params)
    # await chatwoot_service.update_custom_attributes(params)


if __name__ == "__main__":
    asyncio.run(main())
