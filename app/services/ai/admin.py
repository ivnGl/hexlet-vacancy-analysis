from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user_display", "messages", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return "Аноним"

    user_display.short_description = "Пользователь"  # type: ignore
