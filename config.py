import os
from dotenv import load_dotenv

load_dotenv()
# letta variables
LETTA_API_KEY = os.getenv("LETTA_API_KEY")
LETTA_BASE_URL = os.getenv("LETTA_BASE_URL") or "https://app.letta.com"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("MODEL") or "zai/glm-4.7"

# chatwoot variables
CHATWOOT_API_KEY = os.getenv("CHATWOOT_API_KEY")
CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL") or "http://localhost:3000"
