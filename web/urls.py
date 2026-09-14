from django.urls import path

from web.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
]