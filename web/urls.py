from django.urls import path

from web.views import HomePageView, ForUsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('for_us/', ForUsView.as_view(), name='for-us'),
]