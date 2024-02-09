from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model
from django.http import HttpResponseForbidden, JsonResponse, Http404
from dal import autocomplete
from .models import Tag, PhoneCode


class Autocomplete(autocomplete.Select2QuerySetView):
    model: type[Model] = None
    field_name: str = None

    def dispatch(self, request, *args, **kwargs):
        super().__init__(**{'create_field': kwargs.get('field'), 'validate_create': True})
        return super().dispatch(request, *args, **kwargs)

    def __check_model_in_url(self) -> None:
        field_name = self.kwargs.get('field')
        allow_models = (Tag, PhoneCode)
        for allow_model in allow_models:
            if self.kwargs.get('model').lower() == allow_model.__name__.lower():
                try:
                    allow_model._meta.get_field(field_name)
                    self.model = allow_model
                    self.field_name = field_name
                    return
                except FieldDoesNotExist:
                    raise Http404()
        else:
            raise Http404()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You do not have permission to access this resource.")

        self.__check_model_in_url()
        qs = self.model.objects.get_queryset().order_by(self.field_name)
        if self.q:
            qs = qs.filter(**{self.field_name + '__istartswith': self.q})
        return qs

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            if e.__context__.messages is not None:
                return JsonResponse(dict(error=e.__context__.messages[0]))
