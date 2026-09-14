from django.urls import path

from orders.views import CreateOrderView, CalendarView

app_name = 'orders'
urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create'),
    path('calendar/', CalendarView.as_view(), name='calendar')
]