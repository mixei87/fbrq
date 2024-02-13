from django.contrib.admin import register, ModelAdmin
from .models import Client, Mailing, Message
from .forms import MailingForm, ClientForm


@register(Client)
class ClientAdmin(ModelAdmin):
    form = ClientForm


@register(Message)
class MessageAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False


@register(Mailing)
class MailingAdmin(ModelAdmin):
    form = MailingForm
