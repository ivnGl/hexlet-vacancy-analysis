import logging
from typing import List

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View
from inertia import InertiaResponse  # type: ignore
from inertia import render as inertia_render

from .exceptions import OpenAIError
from .models import ChatMessage
from .openrouter import OpenRouterChat

logger = logging.getLogger(__name__)


class AIAssistantView(View):
    def get(self, request: HttpRequest) -> InertiaResponse:
        messages: List[dict[str, str]] = self.get_messages(request)
        return inertia_render(
            request,
            "AIAssistantPage",
            props={
                "messages": messages,
            },
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        message = request.POST.get("message")
        if message is None:
            return JsonResponse({"error": "Message is required"}, status=400)

        messages: List[dict[str, str]] = self.get_messages(request)
        chat: OpenRouterChat = OpenRouterChat(
            api_key=settings.AI_API_KEY,
            messages=messages,
        )

        try:
            responce = chat.send_message(message)
        except TimeoutError:
            logger.error("Превышено время обращения к openAI")
            return JsonResponse({"error": "Request timed out"}, status=504)
        except OpenAIError as e:
            logger.error(str(e))
            return JsonResponse({"error": "OpenAI error"}, status=500)
        except Exception as e:
            logger.error(f"Ошибка при запросе к openAI: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

        messages = chat.messages

        user = request.user if request.user.is_authenticated else None
        cookie_hash = hash(request.COOKIES.get(settings.CSRF_COOKIE_NAME))

        try:
            if user:
                obj, created = ChatMessage.objects.update_or_create(
                    user=user,
                    defaults={
                        "messages": messages,
                        "cookie_hash": cookie_hash,
                    },
                )
            else:
                obj, created = ChatMessage.objects.update_or_create(
                    cookie_hash=cookie_hash,
                    defaults={
                        "messages": messages,
                        "user": None,
                    },
                )
        except Exception as e:
            logger.error(f"Ошибка при обновлении или сохранении: {str(e)}")
            JsonResponse({"error": str(e)}, status=500)

        if created:
            logger.info(f"Создана новая запись: {obj.pk}")
        else:
            logger.info(f"Обновлена существующая запись: {obj.pk}")

        return JsonResponse({"message": responce}, status=200)

    def get_messages(self, request: HttpRequest) -> List[dict[str, str]]:
        if request.user.is_authenticated:
            return ChatMessage.objects.filter(user=request.user)[0].messages
        else:
            try:
                cookie_hash = hash(request.COOKIES[settings.CSRF_COOKIE_NAME])
                return ChatMessage.objects.filter(cookie_hash=cookie_hash)[0].messages
            except IndexError:
                return []
