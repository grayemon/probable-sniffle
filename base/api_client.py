import httpx
from utils.logger import setup_logger
from typing import Any, Dict, Optional


class APIClient:
    """
    Centralized async API client for all tools.
    Handles GET/POST requests, error handling, and logging.
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        auth_header_name: str = "X-API-Key",
        auth_header_prefix: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.auth_header_name = auth_header_name
        self.auth_header_prefix = auth_header_prefix
        self.logger = setup_logger("APIClient")

    def _build_headers(
        self, extra_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            if self.auth_header_prefix:
                headers[self.auth_header_name] = (
                    f"{self.auth_header_prefix} {self.api_key}"
                )
            else:
                headers[self.auth_header_name] = self.api_key
            # Log auth header for debugging (mask the key for security)
            masked_key = (
                self.api_key[:4] + "..." + self.api_key[-4:]
                if len(self.api_key) > 8
                else "***"
            )
            self.logger.info(f"Auth header: {self.auth_header_name}={masked_key}")
        else:
            self.logger.warning("No API key provided!")
        if extra_headers:
            headers.update(extra_headers)
        return headers

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"GET {url} params={params}")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, params=params, headers=self._build_headers(headers)
            )
            response.raise_for_status()
            return response.json()

    async def post(
        self,
        endpoint: str,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        api_key: Optional[str] = None,
    ) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"POST {url} data={data}")
        # Use provided api_key if available, otherwise use default
        original_api_key = self.api_key
        if api_key:
            self.api_key = api_key
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=data, headers=self._build_headers(headers)
                )
                response.raise_for_status()
                # Handle empty response body
                if not response.content:
                    return None
                return response.json()
        finally:
            # Restore original api_key
            self.api_key = original_api_key
