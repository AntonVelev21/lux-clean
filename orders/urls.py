from django.urls import path

from orders.views import CreateOrderView, CalendarView, OrderConfirmationView

app_name = 'orders'
urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('confirmation/', OrderConfirmationView.as_view(), name='confirmation'),
]