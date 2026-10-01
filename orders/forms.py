from datetime import timedelta

from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils import timezone

from orders.models import Order


class OrderCreateForm(ModelForm):
    FIRST_WORKING_HOUR = 9
    LAST_WORKING_HOUR = 17

    class Meta:
        model = Order
        exclude = ['created_at', 'updated_at', 'status', 'total_price', 'total_execution_time_in_minutes']
        labels = {
            'full_name': 'Вашето име',
            'phone_number': 'Телефонен номер',
            'email': 'Имейл',
            'city': 'Изберете град',
            'address': 'Вашият адрес',
            'requested_date': 'Желаните от вас дата и час (ориентировъчен)'
        }

        error_messages = {
            'full_name': {
                'required': 'Моля, въведете Вашето име.',
            },
            'phone_number': {
                'required': 'Моля, въведете телефонен номер за връзка.',
            },
            'email': {
                'required': 'Моля, въведете Вашия имейл адрес.',
                'invalid': 'Въведете валиден имейл адрес.',
            },
            'city': {
                'required': 'Моля, изберете град от списъка.',
            },
            'address': {
                'required': 'Моля, въведете Вашия адрес.',
            },
            'requested_date': {
                'required': 'Моля, изберете дата и час.',
            },
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_time_field = self.fields['requested_date']
        date_time_field.widget.input_type = 'datetime-local'


    def clean_requested_date(self):
        requested_date = self.cleaned_data.get('requested_date')
        if not requested_date:
            return requested_date

        now = timezone.now()

        if requested_date < now:
            raise ValidationError('Моля изберете бъдещи час и дата.')


        if requested_date.hour > self.LAST_WORKING_HOUR:
            raise ValidationError('Избраният от Вас час не е в работното ни време. Моля, изберете час преди 17:00.')


        if requested_date.hour < self.FIRST_WORKING_HOUR:
            raise ValidationError('Избраният от Вас час не е в работното ни време. Моля, изберете час след 9:00.')

        return requested_date



