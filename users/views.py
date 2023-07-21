import json
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView


User = get_user_model()

class Users(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context["locations"] = json.loads(serialize("geojson", users))
        return context
