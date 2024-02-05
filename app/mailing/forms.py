from django.forms import ModelForm, CharField
from dal import autocomplete
from .models import Client


class ClientForm(ModelForm):
    phone = CharField(max_length=12)

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
        widgets = {'tag': autocomplete.ModelSelect2(url='tag-autocomplete')}
