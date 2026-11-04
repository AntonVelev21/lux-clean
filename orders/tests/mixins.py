from datetime import timedelta
from core.choices.city_choices import CityChoices
from orders.models import Order, OrderItem, ReservedHours
from services.tests.mixins import ServiceCreateMixin
from django.utils import timezone



class OrderCreateMixin(ServiceCreateMixin):
    FIRST_WORKING_HOUR = 9
    LAST_WORKING_HOUR = 17


    def create_valid_requested_date(self):
        example_date = timezone.now()
        hour = int(example_date.hour)

        if self.LAST_WORKING_HOUR > hour > self.FIRST_WORKING_HOUR:
            return example_date

        elif hour > self.LAST_WORKING_HOUR:
            example_date += timedelta(days=1)
            hours_to_go_back = (hour - self.LAST_WORKING_HOUR) - 1
            example_date -= timedelta(hours=hours_to_go_back)

        elif hour < self.FIRST_WORKING_HOUR:
            hours_till_opening = (self.FIRST_WORKING_HOUR - hour) + 1
            example_date += timedelta(hours=hours_till_opening)

        return example_date


    def create_order(self, **kwargs):
        defaults = {
            'full_name': 'Anton Antonov Velev',
            'phone_number': '088290940',
            'email': 'velevanton80@gmail.com',
            'city': CityChoices.SOFIA,
            'address': 'кв. Горна баня, ул. Невен 1Б',
            'requested_date': self.create_valid_requested_date(),
            'total_price': 1000,
            'total_execution_time_in_minutes': 120
        }
        defaults.update(kwargs)

        return Order.objects.create(**defaults)


    def create_order_item(self, **kwargs):
        defaults = {
            'order': self.create_order(),
            'service': self.create_service_variant(),
            'quantity': 3
        }
        defaults.update(kwargs)

        return OrderItem.objects.create(**defaults)


    def create_reserved_hours(self, **kwargs):
        defaults = {
            'order': self.create_order(),
            'start_hour': self.create_valid_requested_date(),
            'end_hour': self.create_valid_requested_date()
        }

        defaults.update(kwargs)

        return ReservedHours.objects.create(**defaults)


    def return_order_create_form_data(self):
        return {
            'full_name': 'Anton Antonov Velev',
            'phone_number': '088290940',
            'email': 'velevanton80@gmail.com',
            'city': CityChoices.SOFIA,
            'address': 'кв. Горна баня, ул. Невен 1Б',
            'requested_date': self.create_valid_requested_date(),
            'total_price': 1000,
            'total_execution_time_in_minutes': 120
        }