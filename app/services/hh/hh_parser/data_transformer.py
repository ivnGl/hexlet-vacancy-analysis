"""Data transformer for converting HH API responses to model data."""

from typing import Any, Dict, Optional, Tuple

from bs4 import BeautifulSoup

from .models import City, Company, Platform


class DataTransformer:
    @staticmethod
    def _format_salary(salary_data: Optional[Dict[str, Any]]) -> str:
        if not salary_data:
            return "По договоренности"

        parts = []
        if salary_data.get("from"):
            parts.append(f"от {salary_data['from']}")
        if salary_data.get("to"):
            parts.append(f"до {salary_data['to']}")
        if salary_data.get("currency"):
            parts.append(salary_data["currency"])

        return " ".join(parts)

    @staticmethod
    def _format_list(items: list, key: str) -> str:
        return ", ".join(item.get(key, "") for item in items if item.get(key))

    @staticmethod
    def _extract_plain_text(html_content: Optional[str]) -> str:
        if not html_content:
            return ""
        return BeautifulSoup(html_content, "html.parser").get_text()

    @staticmethod
    def _safe_nested_get(data: Optional[Dict[str, Any]], *keys: str) -> Any:
        if not data:
            return None

        current = data
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
            if current is None:
                return None

        return current


class HHDataTransformer(DataTransformer):
    @staticmethod
    def transform_vacancy_data(item: Dict[str, Any]) -> Dict[str, Any]:
        platform, _ = Platform.objects.get_or_create(name=Platform.HH)
        company = HHDataTransformer._extract_company(item)
        city, full_address = HHDataTransformer._extract_city_and_address(
            item.get("address")
        )

        return {
            "platform": platform,
            "company": company,
            "city": city,
            "platform_vacancy_id": f"{Platform.HH}{item.get('id')}",
            "title": item.get("name"),
            "salary": HHDataTransformer._format_salary(item.get("salary")),
            "url": item.get("alternate_url"),
            "experience": HHDataTransformer._safe_nested_get(
                item, "experience", "name"
            ),
            "schedule": HHDataTransformer._safe_nested_get(
                item, "schedule", "name"
            ),
            "work_format": HHDataTransformer._format_list(
                item.get("work_format", []), "name"
            ),
            "skills": HHDataTransformer._format_list(
                item.get("key_skills", []), "name"
            ),
            "education": HHDataTransformer._safe_nested_get(
                item, "education", "level", "name"
            ),
            "description": HHDataTransformer._extract_plain_text(
                item.get("description")
            ),
            "address": full_address,
            "employment": HHDataTransformer._safe_nested_get(
                item, "employment", "name"
            ),
            "contacts": item.get("contacts"),
            "published_at": item.get("published_at"),
        }

    @staticmethod
    def _extract_company(item: Dict[str, Any]) -> Optional[Company]:
        employer_name = item.get("employer", {}).get("name")
        if not employer_name:
            return None
        company, _ = Company.objects.get_or_create(name=employer_name)
        return company

    @staticmethod
    def _extract_city_and_address(
        address: Optional[Dict[str, Any]],
    ) -> Tuple[Optional[City], Optional[str]]:
        if not address:
            return None, None

        city_name = address.get("city")
        city = None
        if city_name:
            city, _ = City.objects.get_or_create(name=city_name)

        return city, address.get("raw")
