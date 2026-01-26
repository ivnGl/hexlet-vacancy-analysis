from django.http import HttpResponse
from django.views import View
from inertia import render as inertia_render

from .utils.paginated_vacancies import get_paginated_vacancies


class VacancyListView(View):
    async def get(self, request):
        pagination_vacancies = await get_paginated_vacancies(request)
        return inertia_render(
            request,
            "VacanciesPage",
            props={
                "vacancies": pagination_vacancies["vacancies"],
                "pagination": pagination_vacancies["pagination"],
            },
        )


class VacancyListView2(View):
    def get(self, request):
        return HttpResponse(
            "This is a plain text response.", content_type="text/plain"
        )
