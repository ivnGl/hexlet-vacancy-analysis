"""Service for managing SuperJob vacancy operations."""

from typing import Any, Dict, List, Tuple

from ...hh.hh_parser.api_client import HHAPIClient
from ...hh.hh_parser.models import Vacancy
from .api_client import SuperJobAPIClient
from .data_transformer import SuperJobDataTransformer


class VacancyService:
    def __init__(
        self,
        api_client,
        transformer
    ):
        self.api_client = api_client
        self.transformer = transformer

    def save_vacancy(self, vacancies):
        saved_count = 0
        errors: List[str] = []

        for item in vacancies:
            try:
                transformed_data = self.transformer.transform_vacancy_data(item)

                Vacancy.objects.update_or_create(
                    platform_vacancy_id=transformed_data["platform_vacancy_id"],
                    defaults=transformed_data,
                )

                saved_count += 1
            except Exception as e:
                errors.append(f"Вакансия не была сохранена: {str(e)}")
                continue

        return saved_count, errors


class SuperJobVacancyService(VacancyService):
    def __init__(
        self,
        api_client: HHAPIClient = None,
        transformer: SuperJobDataTransformer = None,
    ):
        super().__init__(api_client, transformer)

    def process_vacancies(
        self, params
    ) -> Tuple[int, List[str]]:

        try:
            vacancies_data = self.api_client.fetch_vacancies(params)
        except Exception as e:
            raise ValueError(
                f"Ошибка при получении списка вакансий: {e}"
            ) from e

        return self.save_vacancy(vacancies_data)


class HHVacancyService(VacancyService):
    def __init__(
        self,
        api_client: HHAPIClient = None,
        transformer: SuperJobDataTransformer = None,
    ):
        super().__init__(api_client, transformer)

    def process_vacancies(
        self, params
    ) -> Tuple[int, List[str]]:
        vacancies_data = []
        try:
            vacancy_ids = self.api_client.fetch_vacancies(params)
            print(vacancy_ids)
            for vacancy_id in vacancy_ids:
                vacancies_data.append(self.api_client.fetch_vacancy_detail(vacancy_id))
        except Exception as e:
            raise ValueError(
                f"Ошибка при получении списка вакансий: {e}"
            ) from e

        return self.save_vacancy(vacancies_data)
