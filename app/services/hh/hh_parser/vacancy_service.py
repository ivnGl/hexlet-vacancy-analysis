from asgiref.sync import sync_to_async

from .models import Vacancy


async def process_vacancies(
    params: dict[str, any],
    fetch_ids_func: callable[[str, int, int], list[str]],
    fetch_detail_func: callable[[str], dict[str, any]],
    transformer_func: callable[[dict[str, any]], dict[str, any]],
) -> tuple[int, list[str]]:
    try:
        vacancy_ids = fetch_ids_func(params)
    except Exception as e:
        raise ValueError(f"Ошибка при получении списка вакансий: {e}") from e

    saved_count = 0
    errors: list[str] = []

    for vacancy_id in vacancy_ids:
        try:
            vacancy_data = fetch_detail_func(vacancy_id)
            transformed_data = transformer_func(vacancy_data)

            await sync_to_async(Vacancy.objects.update_or_create)(
                platform_vacancy_id=transformed_data["platform_vacancy_id"],
                defaults=transformed_data,
            )

            saved_count += 1
        except Exception as e:
            errors.append(f"Вакансия {vacancy_id}: {str(e)}")
            continue

    return saved_count, errors
