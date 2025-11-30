"""API client for SuperJob API."""
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

from ...hh.hh_parser.api_client import APIClient

load_dotenv()

BASE_URL = "https://api.superjob.ru/2.0/vacancies"
REQUEST_TIMEOUT = 10


class SuperJobAPIClient(APIClient):
    """API client for SuperJob platform."""

    def __init__(self, timeout: int = REQUEST_TIMEOUT):
        secret_key = os.getenv("SJ_KEY")
        if not secret_key:
            raise ValueError("SJ_KEY environment variable is not set")
        headers = {"X-Api-App-Id": secret_key}
        super().__init__(BASE_URL, headers, timeout)

    def fetch_vacancies(
        self, keyword: str, town: str = "Moscow", count: int = 4
    ) -> List[Dict[str, Any]]:

        params = {
            "keyword": keyword,
            "town": town,
            "count": count,
        }
        data = self.get(self.base_url, params)
        return data.get("objects", [])

