from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from base.models import (
    WebhookEvent,
    WebhookEventAdapter,
    MessageCreated,
    MessageUpdated,
    WebwidgetTriggered,
)
from services.chatwoot import chatwoot_service
from config.settings import settings
import logging
import uvicorn

# Debug: Verify API key is loaded
logger = logging.getLogger(__name__)
logger.info(
    f"webhook.py - CHATWOOT_API_KEY: {settings.chatwoot_agent_bot_api_key[:4] + '...' + settings.chatwoot_agent_bot_api_key[-4:] if settings.chatwoot_agent_bot_api_key else 'None'}"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Chatwoot Webhook Receiver")


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        status_code=200, content={"message": "Chatwoot Webhook Receiver is running"}
    )


@app.post(f"/{settings.webhook_endpoint.lstrip('/')}")
async def receive_webhook(request: Request):
    """
    Receive and validate webhook data
    """
    try:
        # Try to parse as JSON
        try:
            json_data = await request.json()

            # Validate with pydantic v2 using discriminated union
            try:
                webhook_data = WebhookEventAdapter.validate_python(json_data)
                logger.info(f"Validated webhook: {webhook_data.event}")

                # Route to event handler
                result = await event_handler(webhook_data)

                return JSONResponse(status_code=200, content=result)
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                return JSONResponse(
                    status_code=400, content={"status": "error", "message": str(e)}
                )

        except Exception as e:
            logger.info(f"Received non-JSON webhook")
            return JSONResponse(
                status_code=200,
                content={"status": "success", "message": "Webhook received (non-JSON)"},
            )

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(status_code=200, content={"status": "healthy"})


# event handler function
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
        # TODO: Forward to Letta
        from base.models import ConversationParams

        message = "message test reply from Letta"
        logger.info(
            f"Sending message to conversation {data.conversation.id if data.conversation else None}"
        )
        if data.account and data.conversation:
            params = ConversationParams(
                account_id=data.account.id, conversation_id=data.conversation.id
            )
            await chatwoot_service.send_message(params, message)

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


# Run app
if __name__ == "__main__":
    uvicorn.run("tests.webhook:app", host="127.0.0.1", port=8111, reload=True)
