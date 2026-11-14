import shutil
from datetime import timedelta
from django.utils import timezone
from django.test.testcases import TestCase
from django.test.utils import override_settings
from orders.forms import OrderCreateForm
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderFormTests(OrderCreateMixin, TestCase):
    FIRST_WORKING_HOUR = 9
    LAST_WORKING_HOUR = 17
    VALID_HOURS = {00, 30}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def _process_test_order_with_invalid_date_and_hour(self, message, date=None):
        form_data = self.return_order_create_form_data()
        if date:
            form_data['requested_date'] = date
        form = OrderCreateForm(data=form_data)
        expected_error_message = message

        self.assertFalse(form.is_valid())
        self.assertIn('requested_date', form.errors)
        self.assertEqual(form.errors['requested_date'][0], expected_error_message)


    def test_order_with_requested_date_in_the_past_fails_form_validation(self):
        date_in_the_past = timezone.now() - timedelta(days=1)
        expected_error_message = 'Моля изберете бъдещи час и дата.'
        self._process_test_order_with_invalid_date_and_hour(date=date_in_the_past, message=expected_error_message)


    def test_order_with_requested_date_hour_smaller_than_the_first_working_hour_fails_form_validation(self):
        date_with_smaller_hour_than_first_working_hour = self.return_requested_date_with_hour_smaller_than_the_first_working_hour()
        expected_error_message = 'Избраният от Вас час не е в работното ни време. Моля, изберете час между 09:00 и 17:30.'
        self._process_test_order_with_invalid_date_and_hour(date=date_with_smaller_hour_than_first_working_hour, message=expected_error_message)


    def test_order_with_requested_date_hour_bigger_than_the_last_working_hour_fails_form_validation(self):
        date_with_bigger_hour_than_last_working_hour = self.return_requested_date_with_hour_bigger_than_the_last_working_hour()
        expected_error_message = 'Избраният от Вас час не е в работното ни време. Моля, изберете час между 09:00 и 17:30.'
        self._process_test_order_with_invalid_date_and_hour(date=date_with_bigger_hour_than_last_working_hour, message=expected_error_message)


    def test_order_with_invalid_requested_date_minutes_fails_form_validation(self):
        date_with_invalid_minutes = self.return_invalid_requested_date()
        expected_error_message = 'Избраният от Вас час не е валиден час за поръчка. Моля, изберете час завършващ на 00 или 30.'
        self._process_test_order_with_invalid_date_and_hour(date=date_with_invalid_minutes, message=expected_error_message)


    def test_order_with_overlapping_requested_date_hours_fails_form_validation(self):
        order = self.create_order()
        expected_error_message = 'Избраният от Вас час се припокрива с друга поръчка. Моля, изберете свободен час от календара.'
        self._process_test_order_with_invalid_date_and_hour(message=expected_error_message)


    def test_order_with_valid_data_passes_validation(self):
        form_data = self.return_order_create_form_data()
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())