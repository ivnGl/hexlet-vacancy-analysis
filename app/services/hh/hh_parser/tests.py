import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

from .models import City, Company, Platform, Vacancy

HH_API_URL = "https://api.hh.ru/vacancies"
HH_HEADERS = {"User-Agent": "HH-User-Agent"}
VACANCY_FETCH_DELAY = 0.3
DEFAULT_QUERY = "Python"
DEFAULT_AREA = 1
DEFAULT_PER_PAGE = 4


def vacancy_list(request):  # noqa
    params: Dict[str, Any] = {
        "text": DEFAULT_QUERY,
        "area": DEFAULT_AREA,
        "per_page": DEFAULT_PER_PAGE,
    }

    try:
        vacancy_ids = _fetch_vacancy_ids(params)
    except requests.RequestException as exc:
        return JsonResponse(
            {"status": "error", "message": f"Ошибка при получении списка вакансий: {exc}"},
            status=500,
        )

    saved_count = 0
    errors: List[str] = []
    platform = _get_platform()

    for vacancy_id in vacancy_ids:
        try:
            time.sleep(VACANCY_FETCH_DELAY)
            item = _fetch_vacancy_detail(vacancy_id)
            defaults = _build_vacancy_defaults(item, platform)

            Vacancy.objects.update_or_create(
                platform_vacancy_id=defaults["platform_vacancy_id"],
                defaults=defaults,
            )
            saved_count += 1
        except Exception as exc:  # noqa: BLE001 - log aggregated errors for now
            errors.append(f"Вакансия {vacancy_id}: {exc}")

    status_code = 200 if saved_count else 500
    status_text = "success" if saved_count else "error"
    message = (
        f"Успешно сохранено {saved_count} вакансий"
        if saved_count
        else "Не удалось сохранить вакансии"
    )

    return JsonResponse(
        {
            "status": status_text,
            "saved_count": saved_count,
            "errors": errors,
            "message": message,
        },
        status=status_code,
    )


def _fetch_vacancy_ids(params: Dict[str, Any]) -> List[str]:
    payload = _perform_request(HH_API_URL, params=params)
    return [item["id"] for item in payload.get("items", [])]


def _fetch_vacancy_detail(vacancy_id: str) -> Dict[str, Any]:
    detail_url = f"{HH_API_URL}/{vacancy_id}"
    return _perform_request(detail_url)


def _perform_request(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = requests.get(url, params=params, headers=HH_HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()


def _get_platform():
    platform, _ = Platform.objects.get_or_create(name=Platform.HH)
    return platform


def _build_vacancy_defaults(item: Dict[str, Any], platform: Platform) -> Dict[str, Any]:
    company = _get_company(item)
    city, full_address = _get_city_and_address(item.get("address"))

    platform_vacancy_id = f"{Platform.HH}{item.get('id')}"

    return {
        "platform": platform,
        "city": city,
        "company": company,
        "platform_vacancy_id": platform_vacancy_id,
        "title": item.get("name"),
        "salary": _format_salary(item.get("salary")),
        "url": item.get("alternate_url"),
        "experience": _safe_nested_get(item, "experience", "name"),
        "schedule": _safe_nested_get(item, "schedule", "name"),
        "work_format": ", ".join(work["name"] for work in item.get("work_format", [])),
        "skills": ", ".join(skill["name"] for skill in item.get("key_skills", [])),
        "education": _safe_nested_get(item, "education", "level", "name"),
        "description": _extract_plain_text(item.get("description")),
        "address": full_address,
        "employment": _safe_nested_get(item, "employment", "name"),
        "contacts": item.get("contacts"),
        "published_at": item.get("published_at"),
    }


def _get_company(item: Dict[str, Any]) -> Optional[Company]:
    employer_name = item.get("employer", {}).get("name")
    if not employer_name:
        return None
    company, _ = Company.objects.get_or_create(name=employer_name)
    return company


def _get_city_and_address(address: Optional[Dict[str, Any]]) -> Tuple[Optional[City], Optional[str]]:
    if not address:
        return None, None

    city_name = address.get("city")
    city = None
    if city_name:
        city, _ = City.objects.get_or_create(name=city_name)

    return city, address.get("raw")


def _format_salary(salary_data: Optional[Dict[str, Any]]) -> str:
    if not salary_data:
        return ""

    parts = []
    if salary_data.get("from"):
        parts.append(f"от {salary_data['from']}")
    if salary_data.get("to"):
        parts.append(f"до {salary_data['to']}")
    if salary_data.get("currency"):
        parts.append(salary_data["currency"])
    return " ".join(parts)


def _extract_plain_text(description: Optional[str]) -> str:
    if not description:
        return ""
    return BeautifulSoup(description, "html.parser").get_text()


def _safe_nested_get(data: Optional[Dict[str, Any]], *keys: str) -> Optional[str]:
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current