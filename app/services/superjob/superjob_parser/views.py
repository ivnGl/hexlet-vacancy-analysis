"""Views for SuperJob parser."""
from app.services.common.view_helpers import process_vacancy_view

from .api_client import SuperJobAPIClient
from .data_transformer import SuperJobDataTransformer
from .vacancy_service import SuperJobVacancyService


def superjob_list(request):
    """Fetch and persist vacancies from SuperJob API."""
    keyword = "Python"
    town = "Moscow"
    count = 4

    def service_factory():
        api_client = SuperJobAPIClient()
        transformer = SuperJobDataTransformer()
        return SuperJobVacancyService(api_client, transformer)

    return process_vacancy_view(
        request,
        service_factory=service_factory,
        service_params={"keyword": keyword, "town": town, "count": count},
    )
