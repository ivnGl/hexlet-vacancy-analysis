import logging

from django.db import DataError, IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..telegram_client import TelegramChannelClient
from .form import ChannelForm
from .models import Channel
from .utils.exists_channel import ExistsTelegramChannel
from .utils.get_data import DataChannel
from .utils.save_data import SaveDataChannel

logger = logging.getLogger(__name__)


class IndexChannelView(View):
    def get(self, request, *args, **kwargs):
        qs = Channel.objects.all()

        status = request.GET.get("status")
        if status in ["active", "error"]:
            qs = qs.filter(status=status)
            logger.info("Фильтрация по status")

        username = request.GET.get("username")
        if username:
            qs = qs.filter(username__icontains=username)
            logger.info("Фильтрация по username")

        qs = qs.order_by("username")

        try:
            channels = qs.values(
                "id", "username", "channel_id", "status", "last_message_id"
            )
        except IntegrityError as e:
            logger.error(f"Ошибка целостности БД: {e}")
        except DataError as e:
            logger.error(f"Ошибка данных при получении: {e}")
        logger.info("Получение списка каналов")
        return JsonResponse(list(channels), safe=False)


class ShowChannelView(View):
    def get(self, request, *args, **kwargs):
        try:
            channel = get_object_or_404(Channel, id=kwargs["pk"])
        except Http404 as e:
            logger.error("Статус 404, запрашиваемой страницы не существует")
            return JsonResponse(
                {"status": "error", "error": "Channel not found", "details": str(e)},
                status=404,
            )
        except IntegrityError as e:
            logger.error(f"Ошибка целостности БД: {e}")
        except DataError as e:
            logger.error(f"Ошибка данных при получении: {e}")

        logger.info("Статус 200, Получена страница канала")
        return JsonResponse(
            {
                "id": channel.id,
                "username": channel.username,
                "channel_id": channel.channel_id,
                "status": channel.status,
                "last_message_id": channel.last_message_id,
            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class AddChannelView(View):
    async def get(self, request, *args, **kwargs):
        form = ChannelForm()
        return JsonResponse({"status": "ok", "form_fields": list(form.fields.keys())})

    async def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        client_wrapper = await TelegramChannelClient.create()
        client = client_wrapper.client
        username = data.get("username")

        exist = ExistsTelegramChannel()
        exists = await exist.check_channel_exists(client, username)

        if not exists:
            logger.error("Канала не существует")
            return JsonResponse(
                {
                    "status": "error",
                    "errors": {"username": ["Канал не найден в Telegram"]},
                }
            )

        entity = await client.get_entity(username)
        data_channel = DataChannel()
        channel_data = await data_channel.get_channel_data(client, entity)

        save_data = SaveDataChannel()
        result = await save_data.save_valid_form(data, channel_data)
        logger.info("Канал успешно добавлен")
        return JsonResponse(result)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteChannelView(View):
    def get(self, request, *args, **kwargs):
        channel_id = kwargs.get("pk")
        channel = get_object_or_404(Channel, id=channel_id)
        return JsonResponse(
            {
                "status": "confirm",
                "message": f"""
            Are you sure you want to delete the channel {channel.username}?
""",
                "channel_id": channel.id,
            }
        )

    def post(self, request, *args, **kwargs):
        confirm = request.POST.get("confirm")
        if confirm != "yes":
            logger.info("Отмена удаления канала пользователем")
            return JsonResponse(
                {"status": "cancelled", "details": "Deleting was calcelled by user"}
            )
        channel_id = kwargs.get("pk")
        channel = get_object_or_404(Channel, id=channel_id)
        try:
            channel.delete()
        except (IntegrityError, DataError) as e:
            logger.error("Ошибка удаления канала")
            return JsonResponse(
                {"status": "error", "error": "Channel not found", "details": str(e)},
                status=200,
            )
        logger.info("Канал успешно удален")
        return JsonResponse({"status": "ok", "details": "The channel was deleted"})
