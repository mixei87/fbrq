import asyncio

from asgiref.sync import sync_to_async, markcoroutinefunction, async_to_sync
# from asyncio import run

from django.utils import timezone
from rest_framework.serializers import ModelSerializer, SlugField, ValidationError, IntegerField, ListField
from .models import Client, Mailing, PhoneCode, Tag
from .generate_mailing import create_mailing_tasks
from logging import getLogger

log = getLogger(__name__)


class ClientSerializer(ModelSerializer):
    tag = SlugField(write_only=True, required=False)

    def create(self, validated_data):
        tag = validated_data.get('tag', None)
        if tag is not None:
            validated_data['tag'], _ = Tag.objects.get_or_create(tag=tag)
        client = Client.objects.create(**validated_data)
        return client

    class Meta:
        model = Client
        fields = ('phone', 'tag', 'timezone')


class MailingSerializer(ModelSerializer):
    phone_codes = ListField(child=IntegerField(min_value=900, max_value=999), write_only=True, required=False)
    tags = ListField(child=SlugField(), write_only=True, required=False)

    @staticmethod
    async def arange(_min, _max):
        # log.debug('arange')
        for i in range(_min, _max + 1):
            # log.debug(f'{i=}')
            yield i
            await asyncio.sleep(0.0)

    async def create_clients(self):
        # log.debug('Creating clients')
        # log.debug(f'{phone=}')

        # await Client.objects.abulk_create(
        #     [Client(phone=phone, timezone='UTC', phone_code=PhoneCode(930))
        #      async for phone in self.arange(79300000000, 79300009900)], ignore_conflicts=True)

        async for phone in self.arange(79300000000, 79300900000):
            await Client.objects.aget_or_create(phone=str(phone), timezone='UTC')
            # client = Client.objects.aget(phone=str(phone))
            # log.debug(f'Client {client.phone}|{client.phone_code}|{client.timezone}|{client.tag} created')

    # async def test(self, phone_codes):
    #     log.debug(phone_codes)
    #     for phone_code in phone_codes:
    #         await PhoneCode.objects.aget_or_create(phone_code=phone_code)
    #         log.debug(f"{phone_code=}")

    def create(self, validated_data):
        async_to_sync(self.create_clients)()

        phone_codes = list(set(validated_data.pop('phone_codes', [])))
        log.debug(phone_codes)
        tags = list(set(validated_data.pop('tags', [])))
        log.debug(tags)
        mailing = Mailing.objects.create(**validated_data)
        # log.debug(mailing)
        # log.debug([PhoneCode(phone_code=code) for code in phone_codes])
        # async_to_sync(self.test)(phone_codes)
        # t = async_to_sync(PhoneCode.objects.abulk_create)
        # t(obj=[PhoneCode(phone_code=code) for code in phone_codes],
        #   ignore_conflicts=True)
        # mailing.filter_phone_code.add(*phone_codes)
        # run(Tag.objects.abulk_create([Tag(tag=tag) for tag in tags], ignore_conflicts=True))
        # mailing.filter_tag.add(*tags)
        # run(create_mailing_tasks(mailing))
        return mailing

    def validate(self, data):
        if data['finish_time'] < timezone.now():
            raise ValidationError({'time': "Error! 'finish_time' < current timezone time"})
        if data['start_time'] > data['finish_time']:
            raise ValidationError({'time': 'Error! start_time > finish_time'})
        return data

    class Meta:
        model = Mailing
        fields = ('start_time', 'finish_time', 'text_msg', 'phone_codes', 'tags')
