import shutil
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.urls.base import reverse
from orders.models import Order
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderViewTests(OrderCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_order_create_with_invalid_variant_arguments(self):
        url = reverse('orders:create')
        data = {
            'fariant_': 1,
            'full_name': 'Anton Velev',
            'phone_number': '0882909408',
            'email': 'velevanton80@gmail.com',
            'city': 'sofia',
            'address': 'ul. Primerna, bl. 207, et.5, ap. 19',
            'requested_date': self.create_valid_requested_date()
        }

        response = self.client.post(url, data=data)
        expected_error_message = 'Моля, изберете поне една услуга от калкулатора.'

        self.assertFalse(Order.objects.filter(address='ul. Primerna, bl. 207, et.5, ap. 19').exists())
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            field=None,
            errors=expected_error_message
        )


    def test_order_create_with_unexisting_variant_id(self):
        ...


    def test_order_create_with_zero_or_negative_service_quantity(self):
        ...


    def test_order_create_with_quantity_not_int(self):
        ...


    def test_total_price_calculates_correct(self):
        ...


    def test_end_hour_calculates_correct(self):
        ...


    def test_discount_appies_correct(self):
        ...


    def test_order_item_creates_correct(self):
        ...


    def test_order_creates_successfully(self):
        ...