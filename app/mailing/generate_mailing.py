from django.db.models import Q
from django.conf import settings
from logging import getLogger
from .models import Mailing, Client, Message
from .tasks import send_mailing_task
from aiohttp import ClientSession
from asyncio import ensure_future, gather

log = getLogger(__name__)


async def create_mailing_tasks(mailing: Mailing) -> None:
    headers_outer_request = {'accept': 'application/json',
                             'Authorization': f"Bearer {settings.JWT_TOKEN}",
                             'Content-Type': 'application/json'
                             }
    async for client in Client.objects.filter(
            Q(phone_code__in=mailing.filter_phone_code.all()) | Q(tag__in=mailing.filter_tag.all())):
        message = await Message.objects.acreate(mailing=mailing, client=client)
        log.info(message.info_message)
        send_mailing_task.apply_async(eta=mailing.start_time, expires=mailing.finish_time
                                      # ,
                                      # kwargs={}
                                      # 'mailing_id': mailing.pk,
                                      #                                       'message_id': message.pk,
                                      #                                       'headers': headers_outer_request}
                                      )
