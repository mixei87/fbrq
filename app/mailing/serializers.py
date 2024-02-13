from rest_framework.serializers import ModelSerializer, SlugField, ValidationError, IntegerField, ListField

from .models import Client, Mailing, PhoneCode, Tag


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

    def create(self, validated_data):
        phone_codes = validated_data.pop('phone_codes', None)
        tags = validated_data.pop('tags', None)
        mailing = Mailing.objects.create(**validated_data)
        if phone_codes is not None:
            for phone_code in phone_codes:
                PhoneCode.objects.get_or_create(phone_code=phone_code)
                mailing.filter_phone_code.add(phone_code)
        if tags is not None:
            for tag in tags:
                Tag.objects.get_or_create(tag=tag)
                mailing.filter_tag.add(tag)
        return mailing

    def validate(self, data):
        if data['start_time'] > data['finish_time']:
            raise ValidationError({'time': 'Error! start_time > finish_time'})
        return data

    class Meta:
        model = Mailing
        fields = ('start_time', 'finish_time', 'text_msg', 'phone_codes', 'tags')
