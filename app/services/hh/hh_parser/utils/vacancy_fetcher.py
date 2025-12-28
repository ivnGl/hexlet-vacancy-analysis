import asyncio
import logging

from app.services.vacancies.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)


async def fetch_hh_vacancies(params):
    base_url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}
    api_client = HTTPClient(base_url, headers)

    async def fetch_vacancy_detail(vacancy_id: str) -> dict[str, any]:
        return await api_client.get(endpoint=vacancy_id)

    data = await api_client.get(params=params)
    if not data.get("items"):
        logger.warning("No vacancy found in hh api")
        raise ValueError("No vacancy found in hh api")
    items = data.get("items")
    tasks = []
    for item in items:
        tasks.append(asyncio.create_task(fetch_vacancy_detail(item["id"])))

    return await asyncio.gather(*tasks)
