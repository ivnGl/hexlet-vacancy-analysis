"""API client for HeadHunter API."""

import asyncio
import time
from typing import Any, Dict, List

import aiohttp


class APIClient:
    def __init__(self, base_url: str, headers: Dict[str, str], timeout: int):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    async def get(self, url: str, params: Dict[str, Any] = None) -> Any:
        async with aiohttp.ClientSession() as session:
            print(f"Reg{url} start")
            await asyncio.sleep(2)
            async with session.get(
                url, params=params, headers=self.headers, timeout=self.timeout
            ) as response:
                response.raise_for_status()
                return await response.json()


BASE_URL = "https://api.hh.ru/vacancies"
HEADERS = {"User-Agent": "HH-User-Agent"}
REQUEST_TIMEOUT = 10
VACANCY_FETCH_DELAY = 0.3


class HHAPIClient(APIClient):
    def __init__(
        self, delay: float = VACANCY_FETCH_DELAY, timeout: int = REQUEST_TIMEOUT
    ):
        super().__init__(BASE_URL, HEADERS, timeout)
        self.delay = delay

    async def fetch_vacancies(
        self, params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        data = await self.get(self.base_url, params)
        items = data.get("items", [])

        tasks = [self.fetch_vacancy_detail(item["id"]) for item in items]
        return await asyncio.gather(*tasks)

    async def fetch_vacancy_detail(self, vacancy_id: str) -> Dict[str, Any]:
        detail_url = f"{self.base_url}/{vacancy_id}"
        return await self.get(detail_url)
