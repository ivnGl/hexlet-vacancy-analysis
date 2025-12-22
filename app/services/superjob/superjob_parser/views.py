from django.http import JsonResponse

from app.services.hh.hh_parser.utils.vacancy_service import process_vacancies

from .utils.api_client import fetch_superjob_vacancies
from .utils.data_transformer import transform_superjob_data


async def superjob_vacancy_parse(request=None, params: dict | None = None):
    vacancies_data = await process_vacancies(
        fetch_superjob_vacancies, transform_superjob_data, params=params
    )
    return JsonResponse(vacancies_data)
