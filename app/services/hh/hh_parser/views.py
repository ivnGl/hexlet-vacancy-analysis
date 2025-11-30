"""Views for HH parser."""

from app.services.common.view_helpers import process_vacancy_view

from ...superjob.superjob_parser.vacancy_service import HHVacancyService
from .api_client import HHAPIClient
from .data_transformer import HHDataTransformer


def vacancy_list(params: dict | None = None):
    """Fetch and persist vacancies from HH API."""

    if params is None:
        params = {
            "text   ": "Python",
            "area": 1,
            "per_page": 1,
            "page": 0,
        }

    print(params)
    def service_factory():
        api_client = HHAPIClient()
        transformer = HHDataTransformer()
        return HHVacancyService(api_client, transformer)

    return process_vacancy_view(
        service_factory=service_factory,
        service_params=params,
    )
