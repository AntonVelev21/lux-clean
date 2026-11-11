from datetime import timedelta, datetime
from core.choices.city_choices import CityChoices
from orders.models import Order, OrderItem
from services.tests.mixins import ServiceCreateMixin
from django.utils import timezone



class OrderCreateMixin(ServiceCreateMixin):
    FIRST_WORKING_HOUR = 9
    LAST_WORKING_HOUR = 17


    def create_valid_requested_date(self):
        example_date = timezone.now() + timedelta(days=1)
        valid_date = datetime(year=example_date.year, month=example_date.month, day=example_date.day, hour=self.FIRST_WORKING_HOUR)
        return valid_date


    def create_valid_end_hour(self):
        requested_date = self.create_valid_requested_date()
        return  requested_date + timedelta(hours=3)


    def create_order(self, **kwargs):
        defaults = {
            'full_name': 'Anton Antonov Velev',
            'phone_number': '088290940',
            'email': 'velevanton80@gmail.com',
            'city': CityChoices.SOFIA,
            'address': 'кв. Горна баня, ул. Невен 1Б',
            'requested_date': self.create_valid_requested_date(),
            'end_hour': self.create_valid_end_hour(),
            'total_price': 1000,
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


    def return_order_create_form_data(self):
        return {
            'full_name': 'Anton Antonov Velev',
            'phone_number': '088290940',
            'email': 'velevanton80@gmail.com',
            'city': CityChoices.SOFIA,
            'address': 'кв. Горна баня, ул. Невен 1Б',
            'requested_date': self.create_valid_requested_date(),
            'end_hour': self.create_valid_end_hour(),
            'total_price': 1000,
        }


    def return_invalid_requested_date(self):
        date = timezone.now() + timedelta(days=1)
        invalid_minutes = 47
        valid_hour = self.FIRST_WORKING_HOUR
        return datetime(year=date.year, month=date.month, day=date.day, hour=valid_hour, minute=invalid_minutes)


    def return_requested_date_with_hour_bigger_than_the_last_working_hour(self):
        now = timezone.now()
        invalid_hour = self.LAST_WORKING_HOUR + 1
        return datetime(now.year, now.month, now.day, hour=invalid_hour)


    def return_requested_date_with_hour_smaller_than_the_first_working_hour(self):
        now = timezone.now() + timedelta(days=1)
        invalid_hour = self.FIRST_WORKING_HOUR - 1
        return datetime(now.year, now.month, now.day, hour=invalid_hour)