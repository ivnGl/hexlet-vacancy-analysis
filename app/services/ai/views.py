import logging

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View
from inertia import InertiaResponse  # type: ignore
from inertia import render as inertia_render

from .services.chat_service import ChatMessageService
from .services.exceptions import OpenAIError
from .services.openrouter import OpenRouterChat

logger = logging.getLogger(__name__)


class AIAssistantView(View):
    """
    Представление для AI-ассистента с поддержкой аутентифицированных
    и анонимных пользователей.
    Обрабатывает отображение страницы и обмен сообщениями с AI через OpenRouter API.
    """

    ai_sercice = OpenRouterChat(
        api_key=settings.AI_API_KEY,
        model=settings.AI_API_MODEL,
        timeout=int(settings.AI_API_TIMEOUT),
    )
    chat_service = ChatMessageService(
        ai_services=ai_sercice,
        max_history_lenght=int(settings.CHAT_MAX_HISTORY_LENGHT),
    )

    def get(self, request: HttpRequest) -> InertiaResponse:
        """
        Отображает страницу ассистента.

        Возвращает страницу AIAssistantPage с историей сообщений пользователя.

        Args:
            request (HttpRequest): Объект запроса

        Returns:
            InertiaResponse: Страница с пропсами сообщений
        """
        messages = self.chat_service.get_user_messages(request)
        return inertia_render(
            request,
            "AIAssistantPage",
            props={
                "messages": messages,
            },
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает новое сообщение от пользователя.

        Отправляет сообщение в AI, сохраняет историю и возвращает ответ.
        Поддерживает аутентифицированных и анонимных пользователей.

        Args:
            request (HttpRequest): Запрос с сообщением

        Returns:
            JsonResponse: Ответ AI или ошибка с соответствующим статусом
        """
        message = request.POST.get("message")
        if message is None:
            return JsonResponse({"error": "Message is required"}, status=400)

        history_user_messages = self.chat_service.get_user_messages(request)
        self.chat_service.set_messages(history_user_messages)

        try:
            response = self.chat_service.get_response_ai(message)
        except TimeoutError as e:
            logger.error(str(e))
            return JsonResponse({"error": str(e)}, status=504)
        except OpenAIError as e:
            logger.error(str(e))
            return JsonResponse({"error": str(e)}, status=500)

        try:
            self.chat_service.save_messages(request)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"message": response}, status=200)
