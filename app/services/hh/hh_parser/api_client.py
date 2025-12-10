"""API client for HeadHunter API."""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

import aiohttp


class APIClientInterface(ABC):
    @abstractmethod
    async def get(self, url: str, params: Dict[str, Any] = None) -> Any:
        pass


class APIClient(APIClientInterface):
    def __init__(
        self, base_url: str, headers: Dict[str, str], timeout: int = 10
    ):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    async def get(
        self, endpoint: str = "", params: Dict[str, Any] = None
    ) -> Any:
        url = f"{self.base_url}/{endpoint}"
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(limit_per_host=10)
        async with aiohttp.ClientSession(
            timeout=timeout, connector=connector
        ) as session:
            async with session.get(
                url, params=params, headers=self.headers
            ) as response:
                response.raise_for_status()
                return await response.json()


async def fetch_hh_vacancies(params):
    base_url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}
    api_client = APIClient(base_url, headers)

    async def fetch_vacancy_detail(vacancy_id: str) -> Dict[str, Any]:
        return await api_client.get(endpoint=vacancy_id)

    data = await api_client.get(params=params)
    items = data.get("items", [])
    tasks = [fetch_vacancy_detail(item["id"]) for item in items]

    return await asyncio.gather(*tasks)
