from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from base.models import WebhookEventAdapter
from services.handlers import event_handler
from config.settings import settings
from utils.logger import setup_logger
import uvicorn
import logging

# Configure logging
logger = setup_logger(__name__)

# Add file handler for troubleshooting
file_handler = logging.FileHandler('main_app.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Create FastAPI app
logger.info(f"Starting Chatwoot Webhook Receiver on port {settings.webhook_port}")
app = FastAPI(title="Chatwoot Webhook Receiver")


@app.middleware("http")
async def log_requests(request, call_next):
    """Log all incoming requests"""
    logger.info(f"Received request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint hit")
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
                # TODO: Improve error handling - add more specific error messages
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
        # TODO: Improve error handling - add retry logic, better logging
        return JSONResponse(
            status_code=500, content={"status": "error", "message": str(e)}
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint hit")
    return JSONResponse(status_code=200, content={"status": "healthy"})


# Run app
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=settings.webhook_port, reload=True)
