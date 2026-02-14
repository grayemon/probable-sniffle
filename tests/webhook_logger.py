from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
from datetime import datetime

app = FastAPI(title="Webhook Logger")


@app.post("/webhook")
async def receive_webhook(request: Request):
    """Receive and log webhook data"""
    json_data = await request.json()

    # Log to file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n\n{'='*50}\n{timestamp}\n{'='*50}\n{json.dumps(json_data, indent=2)}\n"

    with open("webhook_log.txt", "a") as f:
        f.write(log_entry)

    print(f"[{timestamp}] Received webhook: {json_data.get('event', 'unknown')}")

    return JSONResponse(status_code=200, content={"status": "success"})


@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={"message": "Webhook Logger is running"})


if __name__ == "__main__":
    print("Starting Webhook Logger on port 8111")
    uvicorn.run("webhook_logger:app", host="127.0.0.1", port=8111, reload=True)
