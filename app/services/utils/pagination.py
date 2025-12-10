import asyncio

from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import Q

from ..hh.hh_parser.models import Vacancy
from ..hh.hh_parser.views import hh_vacancy_parse
from ..superjob.superjob_parser.views import superjob_vacancy_parse

VACANCIES_PER_PAGE = 2
HH_AREA_DEFAULT = 1


@sync_to_async
def get_search_vacancies(search_query: str = "") -> list[dict[str, str]]:
    qs = Vacancy.objects.select_related("company", "city", "platform")

    if search_query:
        qs = qs.filter(
            Q(title__icontains=search_query)
            | Q(company__name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    return [
        {
            "platform": v.platform.name if v.platform else "",
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


async def get_pagination(request):
    page_number = int(request.GET.get("page", 1))
    search_query = request.GET.get("search", "").strip()

    vacancies = await get_search_vacancies(search_query)
    paginator = Paginator(vacancies, VACANCIES_PER_PAGE)
    page_obj = paginator.get_page(page_number)

    if page_obj.number == paginator.num_pages:
        hh_params = {
            "text": search_query,
            "per_page": VACANCIES_PER_PAGE,
            "page": page_obj.number - 1,
            "order_by": "publication_time",
        }
        superjob_params = {
            "keyword": search_query,
            "count": VACANCIES_PER_PAGE,
            "page": page_obj.number - 1,
        }

        await asyncio.gather(
            hh_vacancy_parse(params=hh_params),
            superjob_vacancy_parse(params=superjob_params),
        )

        return await get_pagination(request)

    return {
        "pagination": {
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
        },
        "vacancies": page_obj.object_list,
    }
