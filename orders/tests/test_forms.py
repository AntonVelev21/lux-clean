import shutil
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.test.testcases import TestCase
from django.test.utils import override_settings
from orders.forms import OrderCreateForm
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderFormTests(OrderCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_order_with_requested_date_in_the_past_fails_form_validation(self):
        date_in_the_past = timezone.now() - timedelta(days=1)
        form_data = self.return_order_create_form_data()
        form_data['requested_date'] = date_in_the_past
        form = OrderCreateForm(data=form_data)
        expected_error_message = 'Моля изберете бъдещи час и дата.'

        self.assertFalse(form.is_valid())
        self.assertIn('requested_date', form.errors)
        self.assertEqual(form.errors['requested_date'][0], expected_error_message)