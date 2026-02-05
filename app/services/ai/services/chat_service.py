import logging

from django.http import HttpRequest

from ..models import ChatMessage
from .exceptions import OpenAIError
from .openrouter import OpenRouterChat

logger = logging.getLogger(__name__)


class ChatMessageService:
    """Сервис для работы с сообщениями чата"""

    def __init__(
        self,
        ai_services: OpenRouterChat,
        messages: list[dict[str, str]] | None = None,
        max_history_lenght: int = 10,
    ) -> None:
        self.ai_services = ai_services
        self.messages = messages or []
        self.max_history_lenght = max_history_lenght

    def get_user_messages(self, request: HttpRequest) -> list[dict[str, str]]:
        """
        Получает историю сообщений пользователя.

        Для аутентифицированных - по пользователю, для анонимных - по session_key.

        Args:
            request (HttpRequest): Объект запроса

        Returns:
            List[dict]: История сообщений или пустой список
        """
        try:
            if request.user.is_authenticated:
                chat_obj = ChatMessage.objects.filter(user=request.user).first()
                if chat_obj is None:
                    return []
                return chat_obj.messages or []
            else:
                session_key = request.session.session_key
                if not session_key:
                    logger.warning(
                        "Сессия не инициализирована для анонимного пользователя"
                    )
                    return []

                chat_obj = ChatMessage.objects.filter(
                    session_key=session_key,
                    user__isnull=True,
                ).first()
                if chat_obj is None:
                    return []
                return chat_obj.messages or []
        except Exception as e:
            logger.error(f"Ошибка при получении сообщений: {str(e)}")
            return []

    def get_messages(self) -> list[dict[str, str]]:
        """
        Возвращает текущую историю сообщений диалога.

        Returns:
            List[dict]: Список сообщений в формате
                        {"role": "user/assistant", "content": "текст"}
        """
        return self.messages

    def set_messages(self, messages: list[dict[str, str]]) -> None:
        """
        Устанавливает историю сообщений диалога.

        Args:
            messages (List[dict]): Новый список сообщений для диалога
        """
        self.messages = messages

    def add_message(self, messages: list[dict[str, str]]) -> None:
        """Добавляет новое сообщение в историю."""
        self.messages.extend(messages)

    def save_messages(self, request: HttpRequest) -> None:
        """Сохраненяет историю сообщений диалога"""
        messages = self.get_messages()
        user = request.user if request.user.is_authenticated else None
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        try:
            if user:
                obj, created = ChatMessage.objects.update_or_create(
                    user=user,
                    defaults={
                        "messages": messages,
                        "session_key": session_key,
                    },
                )
            else:
                obj, created = ChatMessage.objects.update_or_create(
                    session_key=session_key,
                    defaults={
                        "messages": messages,
                        "user": None,
                    },
                )
        except Exception as e:
            logger.error(f"Ошибка при обновлении или сохранении: {str(e)}")
            raise

        if created:
            logger.info(f"Создана новая запись: {obj.pk}")
        else:
            logger.info(f"Обновлена существующая запись: {obj.pk}")

    def get_response_ai(self, message: str) -> str:
        """Получает ответ от AI и обновляет историю сообщений."""
        try:
            assistant_message = self.ai_services.get_response(
                message, self.get_messages()
            )
        except (TimeoutError, OpenAIError):
            raise
        self.add_message([{"role": "user", "content": message}])
        self.add_message([{"role": "assistant", "content": assistant_message}])
        self.clear_old_messages()
        return assistant_message

    def clear_old_messages(self) -> None:
        """Очищает старые сообщенияю если история превышает максимальную длину."""
        if len(self.messages) > self.max_history_lenght * 2:
            self.messages = [self.messages[0]] + self.messages[
                -(self.max_history_lenght * 2) :
            ]
