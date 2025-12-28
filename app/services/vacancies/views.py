from django.views import View
from inertia import render as inertia_render

from .utils.pagination_vacancies import get_pagination_vacancies


class VacancyList(View):
    async def get(self, request):
        pagination_vacancies = await get_pagination_vacancies(request)
        return inertia_render(
            request,
            "VacancyPage",
            props={
                "vacancies": pagination_vacancies["vacancies"],
                "pagination": pagination_vacancies["pagination"],
            },
        )
