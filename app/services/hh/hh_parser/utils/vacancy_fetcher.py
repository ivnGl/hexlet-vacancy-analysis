import logging

from app.services.vacancies.utils.http_client import HTTPClient

logger = logging.getLogger(__name__)


async def fetch_hh_vacancies(params):
    base_url = "https://api.hh.ru/vacancies"
    headers = {"User-Agent": "HH-User-Agent"}
    api_client = HTTPClient(base_url, headers)
    urls = [base_url]

    responses = await api_client.get(urls=urls, params=params)

    if not responses[0].get("items"):
        logger.warning("No vacancy found in hh api")
        raise ValueError("No vacancy found in hh api")

    vacancies = responses[0].get("items")
    urls = [f"{base_url}/{vacancy['id']}" for vacancy in vacancies]
    return await api_client.get(urls=urls)
