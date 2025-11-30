"""Data transformer for converting SuperJob API responses to model data."""

from datetime import datetime
from typing import Any, Dict, Optional

from ...hh.hh_parser.data_transformer import DataTransformer
from ...hh.hh_parser.models import City, Company, Platform


class SuperJobDataTransformer(DataTransformer):
    """Data transformer for SuperJob API responses."""

    @staticmethod
    def transform_vacancy_data(item: Dict[str, Any]) -> Dict[str, Any]:
        platform, _ = Platform.objects.get_or_create(name=Platform.SUPER_JOB)
        company = SuperJobDataTransformer._extract_company(item)
        city = SuperJobDataTransformer._extract_city(item.get("town"))
        salary = SuperJobDataTransformer._format_salary(
            {
                "from": item.get("payment_from"),
                "to": item.get("payment_to"),
                "currency": item.get("currency"),
            }
        )
        return {
            "platform": platform,
            "company": company,
            "city": city,
            "platform_vacancy_id": f"{Platform.SUPER_JOB}{item.get('id')}",
            "title": item.get("profession"),
            "salary": salary,
            "url": item.get("link"),
            "experience": SuperJobDataTransformer._safe_nested_get(
                item, "experience", "title"
            ),
            "schedule": SuperJobDataTransformer._safe_nested_get(
                item, "type_of_work", "title"
            ),
            "work_format": SuperJobDataTransformer._safe_nested_get(
                item, "place_of_work", "title"
            ),
            "skills": SuperJobDataTransformer._format_skills(
                item.get("candidat")
            ),
            "education": SuperJobDataTransformer._safe_nested_get(
                item, "education", "title"
            ),
            "description": SuperJobDataTransformer._extract_plain_text(
                item.get("vacancyRichText")
            ),
            "address": item.get("address"),
            "employment": SuperJobDataTransformer._safe_nested_get(
                item, "type_of_work", "title"
            ),
            "contacts": item.get("phone"),
            "published_at": SuperJobDataTransformer._parse_published_at(
                item.get("date_published")
            ),
        }

    @staticmethod
    def _extract_company(item: Dict[str, Any]) -> Optional[Company]:
        company_data = item.get("client", {})
        company_name = company_data.get("title")
        if not company_name:
            return None
        company, _ = Company.objects.get_or_create(name=company_name)
        return company

    @staticmethod
    def _extract_city(town_data: Optional[Dict[str, Any]]) -> Optional[City]:
        if not town_data:
            return None
        city_name = town_data.get("title")
        if not city_name:
            return None
        city, _ = City.objects.get_or_create(name=city_name)
        return city

    @staticmethod
    def _format_skills(skills_data: Optional[Any]) -> Optional[str]:
        if not skills_data:
            return None
        if isinstance(skills_data, str):
            return skills_data
        return str(skills_data)

    @staticmethod
    def _parse_published_at(timestamp: Optional[int]) -> Optional[datetime]:
        if not timestamp:
            return None
        return datetime.fromtimestamp(timestamp)
