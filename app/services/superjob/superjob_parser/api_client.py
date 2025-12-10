"""API client for SuperJob API."""

import os

from dotenv import load_dotenv

from ...hh.hh_parser.api_client import APIClient

load_dotenv()


REQUEST_TIMEOUT = 10


async def fetch_superjob_vacancies(params):
    """API client for SuperJob platform."""

    secret_key = os.getenv("SUPERJOB_KEY")
    if not secret_key:
        raise ValueError("SUPERJOB_KEY environment variable is not set")
    base_url = "https://api.superjob.ru/2.0/vacancies"
    headers = {"X-Api-App-Id": secret_key}
    api_client = APIClient(base_url, headers)

    data = await api_client.get(params=params)
    return data.get("objects", [])
