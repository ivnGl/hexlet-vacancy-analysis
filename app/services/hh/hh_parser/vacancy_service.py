from typing import Any, Callable, Dict, List, Tuple

from asgiref.sync import sync_to_async

from .models import Vacancy


#@sync_to_async
async def process_vacancies(
    params: Dict[str, Any],
    fetch_ids_func: Callable[[str, int, int], List[str]],
    fetch_detail_func: Callable[[str], Dict[str, Any]],
    transformer_func: Callable[[Dict[str, Any]], Dict[str, Any]],
) -> Tuple[int, List[str]]:
    try:
        vacancy_ids = fetch_ids_func(params)
    except Exception as e:
        raise ValueError(f"Ошибка при получении списка вакансий: {e}") from e

    saved_count = 0
    errors: List[str] = []

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
