from app.services.hh.hh_parser.utils.vacancy_parser import vacancy_parser

from .utils.api_client import fetch_superjob_vacancies
from .utils.data_transformer import transform_superjob_data


async def superjob_vacancy_parse(request=None, params: dict | None = None):
    return await vacancy_parser(
        fetch_superjob_vacancies, transform_superjob_data, params=params
    )
