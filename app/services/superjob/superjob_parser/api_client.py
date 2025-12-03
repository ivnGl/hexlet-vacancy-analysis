"""API client for SuperJob API."""

import os
from typing import Any, Dict, List

from dotenv import load_dotenv

from ...hh.hh_parser.api_client import APIClient

load_dotenv()

BASE_URL = "https://api.superjob.ru/2.0/vacancies"
REQUEST_TIMEOUT = 10


class SuperJobAPIClient(APIClient):
    """API client for SuperJob platform."""

    def __init__(self, timeout: int = REQUEST_TIMEOUT):
        secret_key = os.getenv("SUPERJOB_KEY")
        if not secret_key:
            raise ValueError("SUPERJOB_KEY environment variable is not set")
        headers = {"X-Api-App-Id": secret_key}
        super().__init__(BASE_URL, headers, timeout)

    def fetch_vacancies(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = self.get(self.base_url, params)
        print(data)
        return data.get("objects", [])
