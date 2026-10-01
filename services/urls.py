from django.urls import path
from services.views import ListServicesView, ServiceDetailView

app_name = 'services'
urlpatterns = [
    path('list/', ListServicesView.as_view(), name='list'),
    path('<str:slug>/', ServiceDetailView.as_view(), name='detail')
]