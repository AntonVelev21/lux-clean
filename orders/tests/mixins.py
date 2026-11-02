from core.choices.city_choices import CityChoices
from orders.models import Order, OrderItem, ReservedHours
from services.tests.mixins import ServiceCreateMixin


class OrderCreateMixin(ServiceCreateMixin):
    @staticmethod
    def create_order(**kwargs):
        defaults = {
            'full_name': 'Anton Antonov Velev',
            'phone_number': '088290940',
            'email': 'velevanton80@gmail.com',
            'city': CityChoices.SOFIA,
            'address': 'кв. Горна баня, ул. Невен 1Б',
            'requested_date': '2026-11-02 16:49:00',
            'total_price': 1000,
            'total_execution_time_in_minutes': 120
        }
        defaults.update(kwargs)

        return Order.objects.create(**defaults)


    def create_order_item(self, **kwargs):
        defaults = {
            'order': self.create_order(),
            'service': self.create_service(),
            'quantity': 3
        }
        defaults.update(kwargs)

        return OrderItem.objects.create(**defaults)


    def create_reserved_hours(self, **kwargs):
        defaults = {
            'order': self.create_order(),
            'start_hour': '2026-11-03 16:00:00',
            'end_hour': '2026-11-02 18:00:00'
        }

        defaults.update(kwargs)

        return ReservedHours.objects.create(**defaults)
