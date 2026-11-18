import shutil
from datetime import timedelta
from io import StringIO
from django.utils import timezone
from django.test.testcases import TestCase
from django.test.utils import override_settings
from core.choices.status_choices import StatusChoices
from orders.models import Order
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT
from django.core.management import call_command


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ChangeOrderStatusTests(OrderCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    @staticmethod
    def _call_command_and_return_result_message():
        out = StringIO()
        call_command('change_orders_status', stdout=out)
        return out.getvalue().rstrip('\n')


    def _process_test_command_does_not_change_order_status(self, order, query_1, query_2, denied=False):
        if denied:
            order.status = StatusChoices.DENIED
            order.save()
        result_message = self._call_command_and_return_result_message()
        expected_message = f'Done. 0 orders -> "FINISHED", 0 orders -> "IN PROCESS".'


        self.assertTrue(query_1.exists())
        self.assertFalse(query_2.exists())
        self.assertEqual(result_message, expected_message)


    def _process_test_command_changes_orders_status(self, expected_message, query_1, query_2):
        result_message = self._call_command_and_return_result_message()
        self.assertFalse(query_1.exists())
        self.assertTrue(query_2.exists())
        self.assertEqual(result_message, expected_message)


    def test_command_changes_orders_status_to_in_process_correct(self):
        now = timezone.now()
        order = self.create_order(requested_date=now)
        expected_message = f'Done. 0 orders -> "FINISHED", 1 orders -> "IN PROCESS".'
        query_for_new = Order.objects.filter(status=StatusChoices.NEW)
        query_for_in_process = Order.objects.filter(status=StatusChoices.IN_PROCESS)

        self._process_test_command_changes_orders_status(expected_message=expected_message, query_1=query_for_new, query_2=query_for_in_process)


    def test_command_changes_orders_status_to_finished_correct(self):
        requested_date_in_the_past = timezone.now() - timedelta(days=1)
        end_hour_in_the_past = requested_date_in_the_past + timedelta(hours=3)
        order = self.create_order(requested_date=requested_date_in_the_past, end_hour=end_hour_in_the_past)
        expected_message = f'Done. 1 orders -> "FINISHED", 0 orders -> "IN PROCESS".'
        query_for_new = Order.objects.filter(status=StatusChoices.NEW)
        query_for_finished = Order.objects.filter(status=StatusChoices.FINISHED)

        self._process_test_command_changes_orders_status(expected_message=expected_message, query_1=query_for_new, query_2=query_for_finished)


    def test_command_does_not_change_order_status_for_upcoming_orders(self):
        order = self.create_order()
        query_for_new = Order.objects.filter(status=StatusChoices.NEW)
        query_for_finished = Order.objects.filter(status=StatusChoices.FINISHED)
        query_for_in_process = Order.objects.filter(status=StatusChoices.IN_PROCESS)

        self.assertFalse(query_for_in_process.exists())
        self._process_test_command_does_not_change_order_status(order=order, query_1=query_for_new, query_2=query_for_finished)



    def test_command_does_not_change_order_status_to_finished_for_denied_orders(self):
        requested_date_in_the_past = timezone.now() - timedelta(days=1)
        end_hour_in_the_past = requested_date_in_the_past + timedelta(hours=3)
        order = self.create_order(requested_date=requested_date_in_the_past, end_hour=end_hour_in_the_past)
        query_for_finished = Order.objects.filter(status=StatusChoices.FINISHED)
        query_for_denied = Order.objects.filter(status=StatusChoices.DENIED)

        self._process_test_command_does_not_change_order_status(order=order, query_1=query_for_denied, query_2=query_for_finished, denied=True)



    def test_command_does_not_change_order_status_to_in_process_for_denied_orders(self):
        now = timezone.now()
        order = self.create_order(requested_date=now)
        query_for_in_process = Order.objects.filter(status=StatusChoices.IN_PROCESS)
        query_for_denied = Order.objects.filter(status=StatusChoices.DENIED)

        self._process_test_command_does_not_change_order_status(order=order, query_1=query_for_denied, query_2=query_for_in_process, denied=True)

