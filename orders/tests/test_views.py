import shutil
from datetime import timedelta
from decimal import Decimal
from django.test.testcases import TestCase
from django.test.utils import override_settings
from django.urls.base import reverse
from orders.models import Order, OrderItem
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderViewTests(OrderCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def _process_request_with_invalid_variant_test(self, data):
        url = reverse('orders:create')
        response = self.client.post(url, data=data)
        expected_error_message = 'Моля, изберете поне една услуга от калкулатора.'
        queryset = Order.objects.filter(address='ul. Primerna, bl. 207, et.5, ap. 19')

        self.assertFalse(queryset.exists())
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            field=None,
            errors=expected_error_message
        )


    def _process_order_create_test(self, variant_price=None):
        data = self.return_order_data()
        url = reverse('orders:create')
        if variant_price:
            variant = self.create_service_variant(price=variant_price)
        else:
            variant = self.create_service_variant()
        data.pop('variant_1')
        data[f'variant_{variant.id}'] = 3
        response = self.client.post(url, data=data)
        queryset = Order.objects.filter(address=data['address'])

        self.assertEqual(response.status_code, 302)
        self.assertTrue(queryset.exists())

        order = Order.objects.get(address=data['address'])

        return order, variant, data


    def test_order_create_with_invalid_variant_arguments(self):
        data = self.return_order_data()
        data.pop('variant_1')
        data['fariant_'] = 1
        self._process_request_with_invalid_variant_test(data=data)


    def test_order_create_with_unexisting_variant_id(self):
        data = self.return_order_data()
        data.pop('variant_1')
        data['variant_99999'] = 1
        self._process_request_with_invalid_variant_test(data=data)


    def test_order_create_with_zero_or_negative_service_quantity(self):
        data = self.return_order_data()
        data['variant_1'] = 0
        self._process_request_with_invalid_variant_test(data=data)


    def test_order_create_with_quantity_not_int(self):
        data = self.return_order_data()
        data['variant_1'] = 'not integer'
        self._process_request_with_invalid_variant_test(data=data)


    def test_total_price_calculates_correct_and_order_creates_successfully(self):
        order, variant, data = self._process_order_create_test()
        quantity = data[f'variant_{variant.id}']
        expected_total_price = variant.price * quantity
        self.assertEqual(order.total_price, expected_total_price)


    def test_end_hour_calculates_correct_and_order_creates_successfully(self):
        order, variant, data = self._process_order_create_test()
        quantity = data[f'variant_{variant.id}']
        expected_duration = timedelta(minutes=variant.execution_time_in_minutes * quantity)
        expected_end_hour = order.requested_date + expected_duration
        self.assertEqual(order.end_hour, expected_end_hour)


    def test_discount_for_orders_with_total_price_gte_200_appies_correct_order_creates_successfully(self):
        order, variant, data = self._process_order_create_test(variant_price=100)
        expected_total_price_after_discount = (3 * 100) * Decimal(str(0.95))
        order = Order.objects.get(address=data['address'])
        self.assertEqual(order.total_price, expected_total_price_after_discount)


    def test_order_item_and_order_creates_successfully_(self):
        order, variant, data = self._process_order_create_test()
        queryset = OrderItem.objects.filter(order=order, service=variant, quantity=3)
        self.assertTrue(queryset.exists())
