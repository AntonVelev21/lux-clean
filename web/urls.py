from django.urls import path

from web.views import HomePageView, ForUsView, ContactsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('about/', ForUsView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts')
]