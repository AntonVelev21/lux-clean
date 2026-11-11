import shutil
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.utils import override_settings
from orders.tests.mixins import OrderCreateMixin
from services.tests.mixins import TEMP_MEDIA_ROOT


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class OrderModelTests(OrderCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_order_with_invalid_phone_number_fails_validation_and_raises_exception(self):
        order_with_invalid_phone_number = self.create_order(phone_number='08829094')
        expected_error_message = 'Моля, въведете валиден телефонен номер.'
        with self.assertRaises(ValidationError) as context:
            order_with_invalid_phone_number.full_clean()

        self.assertEqual(context.exception.messages[0], expected_error_message)


    def test_order_with_valid_phone_number_passes_validation(self):
        order = self.create_order(phone_number='0882909408')

        try:
            order.full_clean()

        except ValidationError:
            self.fail('Validation failed during full_clean()! Order with valid phone number does not pass validation!')


    def test_order_item_passes_validation(self):
        order_item = self.create_order_item()

        try:
            order_item.full_clean()

        except ValidationError:
            self.fail('Validation failed during full_clean()! Order Item with valid data does not pass validation!')





