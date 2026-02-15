from pathlib import Path
from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
from contextlib import asynccontextmanager
from utils.logger import setup_logger

# Initialize logger
log_path = Path(__file__).parent / "server.log"
logger = setup_logger(name="server", log_file=str(log_path))

PORT = 3001


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"[START] Server is live at: http://localhost:{PORT}")
    logger.info("[INFO] Logging active. Press Ctrl+C to stop.")
    yield
    # Shutdown
    logger.info("[STOP] Shutting down server gracefully... Goodbye!")


app = FastAPI(lifespan=lifespan)


# Mount static directory (like http.server does automatically)
# Place your index.html and other files inside a "static" folder
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    status_code = response.status_code

    logger.info(
        f"[{request.client.host}] "
        f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - "
        f"{request.method} {request.url.path} -> {status_code}"
    )
    return response


@app.get("/")
async def root():
    # Redirect root path to index.html explicitly
    return RedirectResponse(url="/index.html")


class LogRequest(BaseModel):
    message: str


@app.post("/log")
async def log_message(log: LogRequest):
    logger.info(f"[CLIENT LOG] {log.message}")
    return {"status": "ok"}


# Mount static directory
# Place your index.html and other files inside a "static" folder
app.mount("/", StaticFiles(directory="tests/server/static", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("tests.server.start:app", host="127.0.0.1", port=PORT, reload=True)
