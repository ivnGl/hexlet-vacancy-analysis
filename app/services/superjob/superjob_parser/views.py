"""Views for SuperJob parser."""

from app.services.common.view_helpers import process_vacancy_view

from .api_client import SuperJobAPIClient
from .data_transformer import SuperJobDataTransformer
from .vacancy_service import VacancyService


async def superjob_vacancy_parse(params: dict | None = None):
    """Fetch and persist vacancies from SuperJob API."""

    def service_factory():
        api_client = SuperJobAPIClient()
        transformer = SuperJobDataTransformer()
        return VacancyService(api_client, transformer)

    return await process_vacancy_view(
        service_factory=service_factory,
        service_params=params,
    )
