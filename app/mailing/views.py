from django import http

from dal import autocomplete
from .models import Tag


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.get_queryset().order_by('tag')
        if self.q:
            qs = qs.filter(tag__istartswith=self.q)
        return qs

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            if e.__context__.messages is not None:
                return http.JsonResponse(dict(error=e.__context__.messages[0]))
