from .views import Autocomplete
from django.urls import path

urlpatterns = [
    path('autocomplete/<slug:model>/<slug:field>/',
         Autocomplete.as_view(), name='autocomplete'),
]
