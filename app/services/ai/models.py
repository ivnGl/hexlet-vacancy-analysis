from django.db import models
from django.utils import timezone

from ..auth.users.models import User


class ChatMessage(models.Model):
    """
    Модель для хранения сообщений в диалоге
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    messages = models.JSONField(blank=True, verbose_name="Сообщения")
    cookie_hash = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"
