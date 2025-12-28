from asgiref.sync import sync_to_async
from django.http import JsonResponse

from app.services.vacancies.models import Vacancy


async def process_vacancies(
    fetch_vacancies, transform_data, params: dict[str, any]
) -> tuple[int, list[str]]:
    saved_count = 0
    errors: list[str] = []
    try:
        vacancies_data = await fetch_vacancies(params)
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": f"Ошибка при парсинге: {str(e)}"},
            status=500,
        )

    for item in vacancies_data:
        try:
            await save_vacancy(transform_data, item)
            saved_count += 1
        except Exception as e:
            errors.append(f"Вакансия не была сохранена: {str(e)}")
            continue
    return JsonResponse(
        {
            "status": "success",
            "vacancies": vacancies_data,
            "message": f"Успешно сохранено {saved_count} вакансий",
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
