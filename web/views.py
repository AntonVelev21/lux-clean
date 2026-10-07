from django.views.generic import TemplateView, ListView


class HomePageView(TemplateView):
    template_name = 'web/home-page.html'


class ForUsView(TemplateView):
    template_name = 'web/about.html'


class ContactsView(TemplateView):
    template_name = 'web/contacts.html'


