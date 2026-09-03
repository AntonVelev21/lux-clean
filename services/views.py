from django.views.generic import ListView
from services.models import Service


class ListServicesView(ListView):
    model = Service
    template_name = 'services/list.html'
    queryset = Service.objects.prefetch_related('variants').all()


