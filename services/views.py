from django.views.generic import ListView, DetailView

from services.models import Service


class ListServicesView(ListView):
    model = Service
    template_name = 'services/list.html'
    queryset = Service.objects.all()



class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/detail.html'
    context_object_name = 'service'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name_parts = {i: name for i, name in enumerate(self.object.name.split())}
        context['name_parts'] = name_parts
        return context


