"""Service for managing SuperJob vacancy operations."""

from typing import List, Tuple

from asgiref.sync import sync_to_async

from ...hh.hh_parser.models import Vacancy


class VacancyService:
    def __init__(
        self,
        api_client,
        transformer,
    ):
        self.api_client = api_client
        self.transformer = transformer

    async def process_vacancies(
        self, params: dict[str, any]
    ) -> Tuple[int, List[str]]:

        vacancies_data = await self.api_client.fetch_vacancies(params)

        saved_count = 0
        errors: List[str] = []

        for item in vacancies_data:

            try:
                await self.save_vacancy(item)

                saved_count += 1
            except Exception as e:
                print(e)
                errors.append(f"Вакансия не была сохранена: {str(e)}")
                continue

        return saved_count, errors

    @sync_to_async
    def save_vacancy(self, item):
        transformed_data = self.transformer.transform_vacancy_data(item)

        Vacancy.objects.update_or_create(
            platform_vacancy_id=transformed_data["platform_vacancy_id"],
            defaults=transformed_data,
        )

