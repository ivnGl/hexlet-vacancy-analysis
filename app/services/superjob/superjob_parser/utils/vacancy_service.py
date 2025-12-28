from asgiref.sync import sync_to_async

from app.services.vacancies.models import Vacancy


async def process_vacancies(
    fetch_vacancies, transform_data, params: dict[str, any]
) -> tuple[int, list[str]]:
    saved_count = 0
    errors: list[str] = []
    vacancies_data = await fetch_vacancies(params)

    for item in vacancies_data:
        try:
            await save_vacancy(transform_data, item)
            saved_count += 1
        except Exception as e:
            errors.append(f"Вакансия не была сохранена: {str(e)}")
            continue
    return {
        "saved_vacancies": saved_count,
        "errors": errors,
        "vacancies": vacancies_data,
    }


@sync_to_async
def save_vacancy(transform_data, item):
    transformed_data = transform_data(item)

    Vacancy.objects.update_or_create(
        platform_vacancy_id=transformed_data["platform_vacancy_id"],
        defaults=transformed_data,
    )
