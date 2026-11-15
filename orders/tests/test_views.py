import shutil
from datetime import timedelta
from decimal import Decimal
from django.test.testcases import TestCase
from django.utils import timezone
from django.core import mail
from django.test.utils import override_settings
from django.urls.base import reverse
from orders.models import Order, OrderItem
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderViewsTests(OrderCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    @staticmethod
    def _format_expected_message(
            full_name,
            requested_date,
            order_items,
            total_price,
            has_discount=False,
    ):
        formatted_date = requested_date.strftime("%d.%m.%Y")
        formatted_time = requested_date.strftime("%H:%M")
        total_price_str = f"{total_price:.2f}"
        text_order_info = "\n".join(
            f"- {service}: {quantity} бр" for service, quantity in order_items
        )

        if has_discount:
            price_after_discount = total_price * Decimal(str(0.95))
            price_after_discount_str = f"{price_after_discount:.2f}"
            price_info_text = (
                f"Стара цена: {total_price_str} € -> "
                f"Цена с приложена 5% отстъпка: {price_after_discount_str} €\n"
            )
        else:
            price_info_text = f"С цена: {total_price_str} €\n"

        return (
            f"Здравейте, {full_name}!\n\n"
            f"Вашата резервация за почистване на:\n{text_order_info}\n\n"
            f"{price_info_text}"
            f"на {formatted_date} от {formatted_time} (*ориентировъчен час) беше успешна!\n\n"
            f"Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите."
        )


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
        with self.captureOnCommitCallbacks(execute=True):
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


    def test_order_confirmation_view_returns_order_confirmation_template_after_order_creation(self):
        self._process_order_create_test()
        url = reverse('orders:confirmation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/confirmation.html')
        self.assertTemplateNotUsed(response, 'web/home-page.html')


    def test_order_confirmation_view_redirects_to_home_page_template_when_order_not_created(self):
        url = reverse('orders:confirmation')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'orders/confirmation.html')


    def test_confirmation_email_sends_correct_when_order_creates_successfully(self):
        order, variant, data = self._process_order_create_test()
        expected_email_subject = 'Потвърждение на вашата резервация'
        expected_receiver = order.email
        order_item = OrderItem.objects.get(order=order, service=variant, quantity=3)
        order_items_data = {order_item.service: order_item.quantity}

        expected_message = self._format_expected_message(
            full_name=order.full_name,
            requested_date=timezone.localtime(order.requested_date),
            order_items=order_items_data.items(),
            total_price=order.total_price,
            has_discount=False
        )

        self.assertEqual(mail.outbox[0].subject, expected_email_subject)
        self.assertEqual(mail.outbox[0].to[0], expected_receiver)
        self.assertEqual(mail.outbox[0].body, expected_message)
