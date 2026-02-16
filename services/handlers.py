from base.models import (
    WebhookEvent,
    MessageCreated,
    MessageUpdated,
    WebwidgetTriggered,
    ConversationParams,
    ConversationCustomAttributes,
)
from services.chatwoot import chatwoot_service
from services.letta import letta_service
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def event_handler(data: WebhookEvent):
    """Route webhook events to appropriate handlers"""
    logger.info(f"Received event: {data.event}")

    if data.event == "message_created":
        return await handle_message_created(data)
    elif data.event == "message_updated":
        return handle_message_updated(data)
    elif data.event == "webwidget_triggered":
        return handle_webwidget_triggered(data)
    elif data.event == "contact_created":
        return {"status": "success", "message": "Contact created event processed"}
    elif data.event == "contact_updated":
        return {"status": "success", "message": "Contact updated event processed"}
    elif data.event == "conversation_created":
        return {"status": "success", "message": "Conversation created event processed"}
    elif data.event == "conversation_updated":
        return {"status": "success", "message": "Conversation updated event processed"}
    else:
        logger.info(f"Unknown event: {data.event}")
        return {
            "status": "success",
            "message": f"Event {data.event} received (no handler)",
            "event": data.event,
        }


async def handle_message_created(data: MessageCreated):
    """Handle message_created event"""
    logger.info(f"Message created: {data.id}, content: {data.content}")

    # Check if message is incoming
    if data.message_type == "incoming":
        logger.info("Processing incoming message")

        if not data.account or not data.conversation:
            logger.warning("Missing account or conversation data")
            return {
                "status": "success",
                "message": "Message created event processed (no account/conversation)",
                "message_id": data.id,
            }

        # Get conversation ID and account ID
        conversation_id = data.conversation.id
        account_id = data.account.id

        # Extract custom attributes from conversation (can be object or dict)
        conversation_data = data.conversation
        if isinstance(conversation_data, dict):
            custom_attrs = conversation_data.get("custom_attributes", {})
        else:
            custom_attrs = getattr(conversation_data, "custom_attributes", {})

        # Check for existing Letta conversation
        letta_conversation_id = custom_attrs.get("letta_conversation_id")

        if not letta_conversation_id:
            logger.info(
                f"No Letta conversation found for Chatwoot conversation {conversation_id}, creating new one"
            )
            # Create new Letta conversation
            letta_conversation_id = await letta_service.create_conversation()

            if not letta_conversation_id:
                logger.error("Failed to create Letta conversation")
                return {
                    "status": "success",
                    "message": "Message created event processed (Letta creation failed)",
                    "message_id": data.id,
                }

            # Update Chatwoot custom attributes with Letta conversation ID
            params = ConversationParams(
                account_id=account_id,
                conversation_id=conversation_id,
                custom_attributes=ConversationCustomAttributes(
                    custom_attributes={"letta_conversation_id": letta_conversation_id}
                ),
            )
            await chatwoot_service.update_custom_attributes(params)
            logger.info(
                f"Stored Letta conversation {letta_conversation_id} for Chatwoot conversation {conversation_id}"
            )

        # Send message to Letta
        logger.info(f"Sending message to Letta conversation {letta_conversation_id}")
        response = await letta_service.send_message(letta_conversation_id, data.content)

        if response:
            # Send Letta response back to Chatwoot
            params = ConversationParams(
                account_id=account_id, conversation_id=conversation_id
            )
            await chatwoot_service.send_message(params, response)
            logger.info(
                f"Sent Letta response to Chatwoot conversation {conversation_id}"
            )
        else:
            logger.warning("No response from Letta")

    return {
        "status": "success",
        "message": "Message created event processed",
        "message_id": data.id,
    }


def handle_message_updated(data: MessageUpdated):
    """Handle message_updated event"""
    logger.info(f"Message updated: {data.id}, status: {data.status}")

    return {
        "status": "success",
        "message": "Message updated event processed",
        "message_id": data.id,
    }


def handle_webwidget_triggered(data: WebwidgetTriggered):
    """Handle webwidget_triggered event"""
    logger.info(f"Web widget triggered, conversation: {data.current_conversation}")

    return {"status": "success", "message": "Web widget triggered event processed"}
