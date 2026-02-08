from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Chatwoot Webhook Receiver")


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        status_code=200,
        content={"message": "Chatwoot Webhook Receiver is running"}
    )


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receive and log webhook data
    """
    try:
        # Get the raw body
        body = await request.body()
        
        # Try to parse as JSON
        try:
            json_data = await request.json()
            logger.info(f"Received webhook data: {json_data}")
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Webhook received",
                    "data": json_data
                }
            )
        except Exception as e:
            logger.info(f"Received non-JSON webhook: {body.decode('utf-8')}")
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Webhook received (non-JSON)",
                    "data": body.decode('utf-8')
                }
            )
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"}
    )

# Run the app
# uvicorn services.chatwoot_webhook:app --reload --port 8111