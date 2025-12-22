from django.http import JsonResponse

from .vacancy_service import process_vacancies


async def vacancy_parser(
    fetch_vacancies, transform_data, params: dict | None = None
):
    try:
        vacancies_data = await process_vacancies(
            fetch_vacancies, transform_data, params=params
        )
        return JsonResponse(
            {
                "status": "success",
                **vacancies_data,
                "message": f"Успешно сохранено {vacancies_data.get('saved_vacancies')} вакансий",
            },
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": f"Ошибка при парсинге: {str(e)}"},
            status=500,
        )
