from ...superjob.superjob_parser.vacancy_service import process_vacancies
from .api_client import fetch_hh_vacancies
from .data_transformer import transform_hh_data


async def hh_vacancy_parse(params: dict | None = None):
    """Fetch and persist vacancies from HH API."""
    print("hh")
    return await process_vacancies(fetch_hh_vacancies, transform_hh_data, params=params)
