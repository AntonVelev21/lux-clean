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
        context['first_part'] = self.object.name.split()[0]
        context['second_part'] = self.object.name.split()[1]
        context['last_part'] = self.object.name.split()[2]
        return context


