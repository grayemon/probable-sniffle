from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
from contextlib import asynccontextmanager

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

PORT = 3001

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"{GREEN}🚀 Server is live at: http://localhost:{PORT}{RESET}")
    print(f"{YELLOW}📜 Logging active. Press Ctrl+C to stop.{RESET}")
    yield
    # Shutdown
    print(f"{RED}\n🛑 Shutting down server gracefully... Goodbye!{RESET}")

app = FastAPI(lifespan=lifespan)

# Mount static directory (like http.server does automatically)
# Place your index.html and other files inside a "static" folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    status_code = response.status_code

    if str(status_code).startswith("2"):
        color = GREEN
    elif str(status_code).startswith("3"):
        color = YELLOW
    else:
        color = RED

    print(f"{color}[{request.client.host}] "
          f"{start_time.strftime('%Y-%m-%d %H:%M:%S')} - "
          f"{request.method} {request.url.path} -> {status_code}{RESET}")
    return response

@app.get("/")
async def root():
    # Redirect root path to index.html
    return RedirectResponse(url="/index.html")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=PORT, reload=True)
