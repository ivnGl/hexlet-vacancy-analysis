from .api_client import fetch_superjob_vacancies
from .data_transformer import transform_superjob_data
from .vacancy_service import process_vacancies


async def superjob_vacancy_parse(params: dict | None = None):
    """Fetch and persist vacancies from SuperJob API."""
    print("super")
    return await process_vacancies(
        fetch_superjob_vacancies, transform_superjob_data, params=params
    )
