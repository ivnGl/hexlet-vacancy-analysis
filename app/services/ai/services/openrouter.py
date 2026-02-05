import logging

import requests
from requests.exceptions import JSONDecodeError, RequestException, Timeout

from .exceptions import OpenAIError

logger = logging.getLogger(__name__)


class OpenRouterChat:
    """Класс для взаимодействия с AI-моделью через OpenRouter API."""

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str, model: str, timeout: int = 10):
        """
        Инициализирует AI API с указанными параметрами.

        Args:
            api_key (str): Ключ API для аутентификации в OpenRouter
            model (str): Модель ИИ для использования
            timeout (int): Таймаут запроса в секундах (по умолчанию 10)
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def get_response(
        self, message: str, history_messages: list[dict[str, str]] | None = None
    ) -> str:
        """
        Отправляет сообщение в AI и возвращает ответ.

        Args:
            message (str): Текст сообщения от пользователя
            history_messages (List[dict]): История сообщений

        Returns:
            str: Ответ от AI-ассистента

        Raises:
            TimeoutError: При превышении времени ожидания ответа
            OpenAIError: При ошибке API OpenRouter (невалидный статус, ошибка в ответе)
        """
        if not history_messages:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
            ]
        else:
            messages = history_messages.copy()
        messages.append({"role": "user", "content": message})

        try:
            response = requests.post(
                self.BASE_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                },
                timeout=self.timeout,
            )
        except Timeout as e:
            error_msg = f"Превышено время ожидания ответа от OpenRouter API: {str(e)}"
            logger.error(error_msg)
            raise TimeoutError(error_msg) from e
        except RequestException as e:
            error_msg = f"Ошибка при запросе к OpenRouter API: {str(e)}"
            logger.error(error_msg)
            raise OpenAIError(error_msg) from e

        try:
            data = response.json()
        except JSONDecodeError as e:
            error_msg = f"Ошибка при декодировании JSON ответа от AI API: {str(e)}"
            logger.error(error_msg)
            raise OpenAIError(error_msg) from e

        if response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Неизвестная ошибка")
            raise OpenAIError(f"{error_msg}, code: {response.status_code}")

        try:
            assistant_message = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            error_msg = f"Некорректный формат ответа от OpenRouter API: {str(e)}"
            logger.error(error_msg)
            raise OpenAIError(error_msg) from e

        return assistant_message
