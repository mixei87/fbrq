from rest_framework.routers import DefaultRouter

from .views import Autocomplete, MailingViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'mailings', MailingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('autocomplete/<slug:model>/<slug:field>/', Autocomplete.as_view(), name='autocomplete'),
]
