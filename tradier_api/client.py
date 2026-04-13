"""Core client for Tradier API."""

import aiohttp
from typing import Optional, Dict, Any
from .auth import get_api_token
from .exceptions import TradierAPIError, AuthenticationError, RateLimitError

class TradierClient:
    """Async Client for interacting with the Tradier API."""

    def __init__(self, sandbox: bool = False, token: Optional[str] = None):
        """
        Initialize the Tradier API Client.
        
        Args:
            sandbox: Whether to use the base sandbox URL.
            token: API Token. If not provided, will securely fetch it.
        """
        self.sandbox = sandbox
        self.base_url = "https://sandbox.tradier.com/v1/" if sandbox else "https://api.tradier.com/v1/"
        self._token = token or get_api_token()
        self._session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def start(self):
        """Initialize the inner aiohttp ClientSession."""
        if self._session is None:
            headers = {
                "Authorization": f"Bearer {self._token}",
                "Accept": "application/json"
            }
            timeout = aiohttp.ClientTimeout(total=15)
            self._session = aiohttp.ClientSession(headers=headers, base_url=self.base_url, timeout=timeout)
            
    async def close(self):
        """Close the inner aiohttp ClientSession."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def _request(self, method: str, path: str, **kwargs) -> bytes:
        """Internal helper for making HTTP requests. Returns raw bytes."""
        if self._session is None:
            await self.start()
            
        async with self._session.request(method, path, **kwargs) as response:
            if response.status == 200:
                return await response.read()
                
            elif response.status == 401:
                raise AuthenticationError("Invalid or missing API token.")
            elif response.status == 429:
                raise RateLimitError("Rate limit exceeded.")
            else:
                text = await response.text()
                raise TradierAPIError(f"HTTP {response.status}: {text}")
                
    async def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> bytes:
        """Make a GET request."""
        return await self._request("GET", path, params=params)

