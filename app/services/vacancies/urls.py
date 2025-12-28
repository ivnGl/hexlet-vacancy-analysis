from django.urls import path

from . import views

urlpatterns = [
    path("", views.VacancyList.as_view(), name="vacancy_list"),
]
