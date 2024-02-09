from django.contrib.admin import register, ModelAdmin
from .models import Client, Message, Mailing
from .forms import ClientForm, MailingForm


@register(Client)
class ClientAdmin(ModelAdmin):
    form = ClientForm


@register(Message)
class MessageAdmin(ModelAdmin):
    pass

    def has_add_permission(self, request):
        return False


@register(Mailing)
class MailingAdmin(ModelAdmin):
    form = MailingForm
