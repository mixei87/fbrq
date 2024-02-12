from dal_select2.widgets import ModelSelect2Multiple
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SlugRelatedField, ValidationError, IntegerField, ListField

from .models import Client, Mailing, PhoneCode


# class ClientSerializer(ModelSerializer):
#     class Meta:
#         model = Client
#         exclude = ('phone_code',)
#
#


class MailingSerializer(ModelSerializer):
    phone_codes = ListField(child=IntegerField(min_value=900, max_value=999), write_only=True, required=False)

    def create(self, validated_data):
        phone_codes = validated_data.pop('phone_codes', None)
        mailing = Mailing.objects.create(**validated_data)
        if phone_codes is not None:
            for phone_code in phone_codes:
                PhoneCode.objects.get_or_create(phone_code=phone_code)
                mailing.filter_phone_code.add(phone_code)
        return mailing

    #
    def validate(self, data):
        if data['start_time'] > data['finish_time']:
            raise ValidationError({'time': 'Error! start_time > finish_time'})
        return data

    class Meta:
        model = Mailing
        fields = ('start_time', 'finish_time', 'text_msg', 'phone_codes')
