import asyncio
import json
from base.api_client import APIClient
from config import LETTA_BASE_URL, LETTA_API_KEY

endpoint = "/v1/agents"
client = APIClient(
    base_url=LETTA_BASE_URL,
    api_key=LETTA_API_KEY,
    auth_header_name="Authorization",
    auth_header_prefix="Bearer",
)


async def test_get():
    response = await client.get(endpoint)
    print(json.dumps(response, indent=4))


if __name__ == "__main__":
    asyncio.run(test_get())
