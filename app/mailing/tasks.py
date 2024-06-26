from logging import getLogger
from celery import shared_task
from .models import Message, Mailing
from aiohttp import ClientSession
from django.conf import settings

log = getLogger(__name__)


@shared_task()
def send_mailing_task():
    log.debug('enter to send_mailing_task')
# async def send_mailing_task(mailing_id: int, message_id: int, headers: dict[str, str]):
#     mailing = Mailing.objects.get(mailing_id)
#     message = Message.objects.get(message_id)
#     # может быть излишне, если celery следит за временем выполнения
#     async with ClientSession() as asession:
#         log.debug('enter to ClientSession')
#         while mailing.can_send:
#             log.debug('enter to while mailing.can_send')
#
#             async with asession.post(f"{settings.OUTER_SERVER_URL}{message.pk}", headers=headers,
#                                      data={'id': message.pk, 'phone': message.client.phone,
#                                            'text': mailing.text_msg}) as response:
#                 answer = await response.json()
#                 if answer['code'] == 0 and answer['message'] == 'OK':
#                     log.debug(f'OK msg_id: {message.pk}')
#                 else:
#                     log.debug(f'FAIL msg_id: {message.pk}')
#                 return
