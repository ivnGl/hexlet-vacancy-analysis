"""API client for HeadHunter API."""

import time

import requests


class APIClient:
    def __init__(self, base_url: str, headers: dict[str, str], timeout: int):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def get(self, url: str, params: dict[str, any] = None) -> any:
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

    def fetch_vacancies(self, params: dict[str, any]) -> list[str]:
        data = self.get(self.base_url, params)
        return [item["id"] for item in data.get("items", [])]

    def fetch_vacancy_detail(self, vacancy_id: str) -> dict[str, any]:
        time.sleep(self.delay)
        detail_url = f"{self.base_url}/{vacancy_id}"
        return self.get(detail_url)
