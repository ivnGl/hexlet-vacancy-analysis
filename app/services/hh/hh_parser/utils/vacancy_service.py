import logging

from asgiref.sync import sync_to_async
from django.http import JsonResponse

from app.services.vacancies.models import Vacancy

logger = logging.getLogger(__name__)


async def process_vacancies(
    fetch_vacancies, transform_data, params: dict[str, any]
) -> JsonResponse:
    try:
        vacancies = await fetch_vacancies(params)
        for vacancy in vacancies:
            await save_vacancy(transform_data, vacancy)
    except ValueError as e:
        return JsonResponse(
            {"status": "error", "message": f"Vacancies not found: {str(e)}"},
            status=404,
        )
    except AttributeError as e:
        return JsonResponse(
            {"status": "error", "message": f"{str(e)}"},
            status=500,
        )
    except RuntimeError as e:
        return JsonResponse(
            {"status": "error", "message": f"{str(e)}"},
            status=500,
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": f"Ошибка при парсинге: {str(e)}"},
            status=500,
        )
    return JsonResponse(
        {
            "status": "success",
            "vacancies": vacancies,
            "message": f"Успешно сохранено {len(vacancies)} вакансий",
            "total": len(vacancies),
        },
        status=200,
    )


@sync_to_async
def save_vacancy(transform_data, item):
    transformed_data = transform_data(item)
    Vacancy.objects.update_or_create(
        platform_vacancy_id=transformed_data["platform_vacancy_id"],
        defaults=transformed_data,
    )
