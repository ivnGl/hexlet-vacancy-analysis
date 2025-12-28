from typing import List

import requests
from django.conf import settings
from requests.exceptions import Timeout

from .exceptions import OpenAIError


class OpenRouterChat:
    """
    Класс для взаимодействия с AI-моделью через OpenRouter API.

    Позволяет отправлять сообщения, получать ответы и управлять историей диалога.
    Поддерживает ограничение длины истории и работу с различными моделями ИИ.
    """

    def __init__(
        self,
        api_key: str,
        model: str = settings.AI_MODEL,
        max_history_lenght: int = settings.AI_MAX_HISTORY_LENGTH,
        messages: List[dict[str, str]] | None = None,
    ):
        """
        Инициализирует чат с указанными параметрами.

        Args:
            api_key (str): Ключ API для аутентификации в OpenRouter
            model (str): Модель ИИ для использования
            max_history_lenght (int): Максимальное количество пар сообщений в истории
            messages (List[dict] | None): История сообщений для продолжения диалога
        """
        self.api_key = api_key
        self.model = model
        self.max_history_lenght = max_history_lenght
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def send_message(self, message: str, timeout: int = settings.AI_API_TIMEOUT) -> str:
        """
        Отправляет сообщение в AI и возвращает ответ.

        Добавляет сообщение в историю, отправляет запрос к API, сохраняет ответ
        и управляет длиной истории диалога.

        Args:
            message (str): Текст сообщения от пользователя
            timeout (int): Таймаут запроса в секундах

        Returns:
            str: Ответ от AI-ассистента

        Raises:
            TimeoutError: При превышении времени ожидания ответа
            OpenAIError: При ошибке API OpenRouter (невалидный статус, ошибка в ответе)
        """
        self.messages.append({"role": "user", "content": message})

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": self.messages[-self.max_history_lenght * 2 :],
                },
                timeout=timeout,
            )
        except Timeout as e:
            raise TimeoutError(e)

        data = response.json()

        if response.status_code != 200:
            raise OpenAIError(
                f"{data['error']['message']}, code: {response.status_code}"
            )

        assistant_message = data["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": assistant_message})

        # Очищаем старые сообщения, если история слишком большая
        if len(self.messages) > self.max_history_lenght * 2:
            self.messages = [self.messages[0]] + self.messages[
                -(self.max_history_lenght * 2) :
            ]

        return assistant_message

    def get_messages(self) -> List[dict[str, str]]:
        """
        Возвращает текущую историю сообщений диалога.

        Returns:
            List[dict]: Список сообщений в формате
                        {"role": "user/assistant", "content": "текст"}
        """
        return self.messages
