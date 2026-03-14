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
import json

logger = setup_logger(__name__)


async def handle_letta_response(
    response: dict,
    letta_conversation_id: str,
    account_id: int,
    conversation_id: int,
):
    """
    Handle Letta response, processing approval requests for client-side tools.

    Args:
        response: Letta API response
        letta_conversation_id: Letta conversation ID
        account_id: Chatwoot account ID
        conversation_id: Chatwoot conversation ID
    """
    messages = response.get("messages", [])

    for msg in messages:
        if msg.get("message_type") == "approval_request_message":
            tool_call = msg.get("tool_call")
            if tool_call and tool_call.get("name") == "send_chatwoot_message":
                logger.info("Received approval request for send_chatwoot_message")

                # Parse tool arguments
                args = json.loads(tool_call.get("arguments", "{}"))
                content = args.get("content", "")
                content_type = args.get("content_type", "text")
                content_attributes = args.get("content_attributes")

                # Execute tool locally (send to Chatwoot)
                params = ConversationParams(
                    account_id=account_id, conversation_id=conversation_id
                )
                result = await chatwoot_service.send_message(
                    params,
                    content,
                    content_type=content_type,
                    content_attributes=content_attributes,
                )

                # Send result back to Letta
                tool_call_id = tool_call.get("tool_call_id")
                status = "success" if result else "error"
                result_message = "Message sent successfully" if result else "Failed to send message"

                await letta_service.send_tool_result(
                    letta_conversation_id, tool_call_id, result_message, status
                )
                logger.info(f"Sent tool result back to Letta: {status}")
            else:
                logger.warning(f"Unknown tool approval request: {tool_call}")
        elif msg.get("message_type") == "assistant_message":
            # Agent responded with text (shouldn't happen with client-side tools)
            content = msg.get("content")
            if content:
                logger.warning(f"Agent responded with text instead of tool: {content[:100]}...")


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

        # Check for existing Letta agent
        letta_agent_id = custom_attrs.get("letta_agent_id")

        if not letta_agent_id:
            logger.info(
                f"No Letta agent found for Chatwoot conversation {conversation_id}, creating new one"
            )
            # Create new Letta agent
            letta_agent_id = await letta_service.create_agent()

            if not letta_agent_id:
                logger.error("Failed to create Letta agent")
                return {
                    "status": "success",
                    "message": "Message created event processed (Letta agent creation failed)",
                    "message_id": data.id,
                }

            # Update Chatwoot custom attributes with Letta agent ID
            params = ConversationParams(
                account_id=account_id,
                conversation_id=conversation_id,
                custom_attributes=ConversationCustomAttributes(
                    custom_attributes={"letta_agent_id": letta_agent_id}
                ),
            )
            await chatwoot_service.update_custom_attributes(params)
            logger.info(
                f"Stored Letta agent {letta_agent_id} for Chatwoot conversation {conversation_id}"
            )

        # Check for existing Letta conversation
        letta_conversation_id = custom_attrs.get("letta_conversation_id")

        if not letta_conversation_id:
            logger.info(
                f"No Letta conversation found for Chatwoot conversation {conversation_id}, creating new one"
            )
            # Create new Letta conversation with the agent
            letta_conversation_id = await letta_service.create_conversation(
                agent_id=letta_agent_id
            )

            if not letta_conversation_id:
                logger.error("Failed to create Letta conversation")
                return {
                    "status": "success",
                    "message": "Message created event processed (Letta conversation creation failed)",
                    "message_id": data.id,
                }

            # Update Chatwoot custom attributes with Letta conversation ID
            params = ConversationParams(
                account_id=account_id,
                conversation_id=conversation_id,
                custom_attributes=ConversationCustomAttributes(
                    custom_attributes={
                        "letta_agent_id": letta_agent_id,
                        "letta_conversation_id": letta_conversation_id,
                    }
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
            # Check for approval request (client-side tool)
            await handle_letta_response(
                response, letta_conversation_id, account_id, conversation_id
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
