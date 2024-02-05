from .models import Client
from .views import TagAutocomplete
from django.urls import path

urlpatterns = [
    path('tag-autocomplete/', TagAutocomplete.as_view(model=Client, create_field='tag', validate_create=True),
         name='tag-autocomplete'),
]
