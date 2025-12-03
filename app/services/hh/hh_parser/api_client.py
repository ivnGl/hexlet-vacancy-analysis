"""API client for HeadHunter API."""

import time
from typing import Any, Dict, List

import requests


class APIClient:
    def __init__(self, base_url: str, headers: Dict[str, str], timeout: int):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def get(self, url: str, params: Dict[str, Any] = None) -> Any:
        response = requests.get(
            url, params=params, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()


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

    def fetch_vacancies(
        self, params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        data = self.get(self.base_url, params)
        return [
            self.fetch_vacancy_detail(item["id"])
            for item in data.get("items", [])
        ]

    def fetch_vacancy_detail(self, vacancy_id: str) -> Dict[str, Any]:
        time.sleep(self.delay)
        detail_url = f"{self.base_url}/{vacancy_id}"
        return self.get(detail_url)
