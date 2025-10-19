from django.http import JsonResponse
from inertia import render as inertia_render

from .services.hh.hh_parser.models import Vacancy


def index(request):
    return inertia_render(
        request,
        "HomePage",
        props={},
    )


def vacancy(request):
    qs = Vacancy.objects.select_related('company', 'city').all()
    vacancies = []
    for vacancy in qs:
        vacancies.append({'title': vacancy.title,
                          'salary': vacancy.salary,
                          'company': vacancy.company.name,
                          'city': vacancy.city.name})
    return inertia_render(
        request,
        "VacancyPage",
        props={'vacancies': vacancies},
    )


def custom_server_error(request):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=500
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=404
    )

