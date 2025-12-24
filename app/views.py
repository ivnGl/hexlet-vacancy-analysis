from django.http import JsonResponse
from inertia import render as inertia_render

from .utils.pagination_vacancies import get_pagination_vacancies


def index(request):
    return inertia_render(request, "HomePage", props={})


async def vacancy(request):
    pagination_vacancies = await get_pagination_vacancies(request)
    return inertia_render(
        request,
        "VacancyPage",
        props={
            "vacancies": pagination_vacancies["vacancies"],
            "pagination": pagination_vacancies["pagination"],
        },
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
