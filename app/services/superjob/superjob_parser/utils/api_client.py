"""API client for SuperJob API."""

import os

from dotenv import load_dotenv

from app.services.hh.hh_parser.utils.api_client import HTTPClient

load_dotenv()


async def fetch_superjob_vacancies(params):
    secret_key = os.getenv("SUPERJOB_KEY")
    if not secret_key:
        raise ValueError("SUPERJOB_KEY environment variable is not set")
    base_url = "https://api.superjob.ru/2.0/vacancies"
    headers = {"X-Api-App-Id": secret_key}
    api_client = HTTPClient(base_url, headers)

    data = await api_client.get(params=params)
    if not data.get("objects"):
        raise ValueError("No data found")
    return data.get("objects")
