from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils import timezone

from orders.models import Order


class OrderCreateForm(ModelForm):
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
            raise ValidationError("Моля изберете бъдещи час и дата.")

        return requested_date

