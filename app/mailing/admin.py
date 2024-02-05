from django.contrib.admin import register, ModelAdmin
from .models import Client, Message, Mailing
from .forms import ClientForm


@register(Client)
class ClientAdmin(ModelAdmin):
    form = ClientForm


@register(Message)
class MessageAdmin(ModelAdmin):
    pass


@register(Mailing)
class MailingAdmin(ModelAdmin):
    pass
