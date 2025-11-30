"""Shared helpers for vacancy views."""
from typing import Any, Callable, Dict

from django.http import JsonResponse


def process_vacancy_view(
    service_factory: Callable[[], Any],
    service_params: Dict[str, Any],
) -> JsonResponse:
    """Process a vacancy view request with shared error handling."""
    service = service_factory()

    try:
        saved_count, errors = service.process_vacancies(service_params)
        return JsonResponse(
            {
                "status": "success",
                "saved_count": saved_count,
                "errors": errors,
                "message": f"Успешно сохранено {saved_count} вакансий",
            },
            status=200,
        )

    except ValueError as exc:
        return JsonResponse(
            {"status": "error", "message": str(exc)},
            status=500,
        )
    except Exception as exc:
        return JsonResponse(
            {"status": "error", "message": f"Ошибка при парсинге: {str(exc)}"},
            status=500,
        )


