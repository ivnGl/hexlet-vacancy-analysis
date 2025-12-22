from django.http import JsonResponse

from app.services.superjob.superjob_parser.utils.vacancy_service import (
    process_vacancies,
)

from .utils.api_client import fetch_hh_vacancies
from .utils.data_transformer import transform_hh_data


async def hh_vacancy_parse(request=None, params: dict | None = None):
    vacancies_data = await process_vacancies(
        fetch_hh_vacancies, transform_hh_data, params=params
    )
    return JsonResponse(
        {
            "status": "success",
            **vacancies_data,
            "message": f"Успешно сохранено {vacancies_data.get('saved_vacancies')} вакансий",
        },
        status=200,
    )
