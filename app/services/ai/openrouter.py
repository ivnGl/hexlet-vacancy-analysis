from typing import List

import requests
from django.conf import settings
from requests.exceptions import Timeout

from .exceptions import OpenAIError


class OpenRouterChat:
    def __init__(
        self,
        api_key: str,
        model: str = settings.AI_MODEL,
        max_history_lenght: int = settings.AI_MAX_HISTORY_LENGTH,
        messages: List[dict[str, str]] | None = None,
    ):
        self.api_key = api_key
        self.model = model
        self.max_history_lenght = max_history_lenght
        if messages is None:
            self.messages = []
        else:
            self.messages = messages

    def send_message(self, message: str, timeout: int = settings.AI_API_TIMEOUT) -> str:
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
        return self.messages
