from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def webhook_receiver(request: Request):
    data = await request.json()
    return {"received_data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8111)
