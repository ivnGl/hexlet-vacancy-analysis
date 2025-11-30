from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from inertia import render as inertia_render

from .services.hh.hh_parser.models import Vacancy
from .services.hh.hh_parser.views import vacancy_list


def index(request):
    return inertia_render(
        request,
        "HomePage",
        props={},
    )


last_page = 1


def vacancy(request):
    VACANCY_PER_PAGE = 2
    HH_VACANCY_PER_PAGE = 4
    PAGE = 0
    global last_page

    page_number = int(request.GET.get("page", 1))
    hh_page_number = int(page_number) - 1

    search = request.GET.get("search", "")

    print(page_number, last_page)

    if page_number == last_page:
        params = {
            "text": search,
            "area": 1,
            "page": hh_page_number,
            "per_page": 4,
        }
        vacancy_list(params=params)

    qs = Vacancy.objects.select_related("company", "city").all()

    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(company__name__icontains=search)
            | Q(description__icontains=search)
        )
    else:
        qs = Vacancy.objects.select_related("company", "city").all()
    vacancies = []
    for vacancy in qs:
        vacancies.append(
            {
                "title": vacancy.title,
                "salary": vacancy.salary,
                "company": vacancy.company.name if vacancy.company else "",
                "city": vacancy.city.name if vacancy.city else "",
                "url": vacancy.url,
            }
        )
    paginator = Paginator(vacancies, VACANCY_PER_PAGE)
    page_obj = paginator.get_page(page_number)


    last_page = paginator.num_pages

    current_page = page_obj.number

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
        {"status": "error", "message": "Internal server error"}, status=500
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"}, status=404
    )
