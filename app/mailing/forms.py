from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField
from dal.autocomplete import ModelSelect2, ModelSelect2Multiple
from .models import Client, Mailing


class ClientForm(ModelForm):
    phone = CharField(max_length=12, label="Телефон")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone.startswith('+'):
            phone = phone[1:]
        elif phone.startswith('8'):
            phone = '7' + phone[1:]
        return phone

    class Meta:
        model = Client
        exclude = ('phone_code',)
        widgets = {'tag': ModelSelect2(url='/mailing/autocomplete/Tag/tag/')}


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        widgets = {
            'filter_tag': ModelSelect2Multiple(url='/mailing/autocomplete/Tag/tag/'),
            'filter_phone_code': ModelSelect2Multiple(url='/mailing/autocomplete/PhoneCode/phone_code/')}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['start_time'] > cleaned_data['finish_time']:
            raise ValidationError('Error! start_time > finish_time')
        return cleaned_data
