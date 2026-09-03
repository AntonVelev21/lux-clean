from django.urls import path
from services.views import ListServicesView

app_name = 'services'
urlpatterns = [
    path('list/', ListServicesView.as_view(), name='list')
]