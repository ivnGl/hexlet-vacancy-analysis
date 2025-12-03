from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from inertia import render as inertia_render

from app.services.superjob.superjob_parser.views import superjob_vacancy_parse

from .services.hh.hh_parser.models import Vacancy
from .services.hh.hh_parser.views import hh_vacancy_parse

VACANCIES_PER_PAGE = 2
HH_AREA_DEFAULT = 1
HH_PER_PAGE_DEFAULT = 4


def index(request):
    """Render home page."""
    return inertia_render(request, "HomePage", props={})


def query_vacancies(search_query: str = "") -> list[dict[str, str]]:
    """Return serialized vacancies filtered by optional search query."""
    qs = Vacancy.objects.select_related("company", "city")

    if search_query:
        qs = qs.filter(
            Q(title__icontains=search_query)
            | Q(company__name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    return [
        {
            "title": v.title,
            "salary": v.salary,
            "company": v.company.name if v.company else "",
            "city": v.city.name if v.city else "",
            "url": v.url,
            "skills": v.skills,
            "experience": v.experience,
            "employment": v.employment,
            "work_format": v.work_format,
            "schedule": v.schedule,
            "description": v.description,
            "address": v.address,
            "contacts": v.contacts,
            "published_at": v.published_at,
        }
        for v in qs
    ]


async def refetch():
    pass


def vacancy(request):
    """Render paginated vacancy list with optional search filtering."""
    page_number = int(request.GET.get("page", 1))
    search_query = request.GET.get("search", "").strip()

    vacancies = query_vacancies(search_query)
    paginator = Paginator(vacancies, VACANCIES_PER_PAGE)
    page_obj = paginator.get_page(page_number)

    """Auto-fetch additional vacancies from HH when user reaches the last page."""
    if page_obj.number == paginator.num_pages:
        params = {
            "text": search_query,
            "area": HH_AREA_DEFAULT,
            "per_page": HH_PER_PAGE_DEFAULT,
            "page": page_obj.number - 1,
        }

        hh_vacancy_parse(params=params)
        superjob_vacancy_parse(params=params)

        """Re-query after new vacancies have been fetched and stored."""
        vacancies = query_vacancies(search_query)
        paginator = Paginator(vacancies, VACANCIES_PER_PAGE)
        page_obj = paginator.get_page(page_number)

    pagination = {
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "next_page_number": page_obj.next_page_number()
        if page_obj.has_next()
        else None,
        "previous_page_number": page_obj.previous_page_number()
        if page_obj.has_previous()
        else None,
    }

    return inertia_render(
        request,
        "VacancyPage",
        props={"vacancies": page_obj.object_list, "pagination": pagination},
    )


def custom_server_error(request):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=500,
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=404,
    )
