from abc import ABC, abstractmethod

import aiohttp

REQUEST_TIMEOUT = 10


class HTTPClientInterface(ABC):
    @abstractmethod
    async def get(self, url: str, params: dict[str, any] = None) -> any:
        pass


class HTTPClient(HTTPClientInterface):
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        timeout: int = REQUEST_TIMEOUT,
    ):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    async def get(
        self, endpoint: str | None = None, params: dict[str, any] = None
    ) -> any:
        url = f"{self.base_url}/{endpoint}" if endpoint else f"{self.base_url}"
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(limit_per_host=1, limit=10)
        async with aiohttp.ClientSession(
            timeout=timeout, connector=connector
        ) as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()
