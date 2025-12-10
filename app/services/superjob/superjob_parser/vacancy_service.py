"""Service for managing SuperJob vacancy operations."""

from typing import List, Tuple

from asgiref.sync import sync_to_async

from ...hh.hh_parser.models import Vacancy


async def process_vacancies(
    fetch_vacancies, transform_data, params: dict[str, any]
) -> Tuple[int, List[str]]:
    vacancies_data = await fetch_vacancies(params)

    saved_count = 0
    errors: List[str] = []

    for item in vacancies_data:
        try:
            await save_vacancy(transform_data, item)

            saved_count += 1
        except Exception as e:
            errors.append(f"Вакансия не была сохранена: {str(e)}")
            continue

    return saved_count, errors


@sync_to_async
def save_vacancy(transform_data, item):

    transformed_data = transform_data(item)

    print(transformed_data["platform_vacancy_id"])

    Vacancy.objects.update_or_create(
        platform_vacancy_id=transformed_data["platform_vacancy_id"],
        defaults=transformed_data,
    )
