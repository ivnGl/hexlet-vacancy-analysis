import datetime

from asgiref.sync import sync_to_async
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from app.services.vacancies.models import Vacancy
from app.services.vacancies.utils.paginated_vacancies import (
    get_search_vacancies,
)
from app.services.vacancies.views import VacancyListView


class VacanciesTest(TestCase):
    def setUp(self):
        self.vacancy = Vacancy.objects.create(
            title="Test python",
            salary=1200,
            published_at=datetime.datetime.now(datetime.UTC),
        )

    def test_vacancy_created(self):
        vacancy = Vacancy.objects.get(title="Test python")

        self.assertEqual(vacancy.salary, "1200")

    async def test_get_search_vacancies(self):
        searched_vacancies = await get_search_vacancies("python")

        self.assertEqual(self.vacancy.title, searched_vacancies[0]["title"])

    async def test_vacancies_list_view(self):
        request = RequestFactory().get('/kjlj')
        middleware = SessionMiddleware(lambda r: r)
        middleware.process_request(request)
        response = await VacancyListView.as_view()(request)
        print(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text="python")

