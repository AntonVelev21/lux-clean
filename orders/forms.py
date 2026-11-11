from datetime import time
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils import timezone
from orders.models import Order


class OrderCreateForm(ModelForm):
    FIRST_WORKING_HOUR = time(9, 0)
    LAST_WORKING_HOUR = time(17, 30)
    VALID_MINUTES = {0, 30}

    class Meta:
        model = Order
        exclude = ['created_at', 'updated_at', 'status', 'total_price', 'end_hour']
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

        local_dt = timezone.localtime(requested_date)
        requested_time = local_dt.time()

        if requested_date < timezone.now():
            raise ValidationError('Моля изберете бъдещи час и дата.')

        if requested_time < self.FIRST_WORKING_HOUR or requested_time > self.LAST_WORKING_HOUR:
            raise ValidationError(
                'Избраният от Вас час не е в работното ни време. Моля, изберете час между 09:00 и 17:30.')

        if local_dt.minute not in self.VALID_MINUTES or local_dt.second != 0:
            raise ValidationError(
                'Избраният от Вас час не е валиден час за поръчка. Моля, изберете час завършващ на 00 или 30.')

        orders = Order.objects.filter(
            requested_date__date=local_dt.date()
        ).only('requested_date', 'end_hour')

        for order in orders:
            start = timezone.localtime(order.requested_date).time()
            end = timezone.localtime(order.end_hour).time()
            if start <= requested_time < end:
                raise ValidationError(
                    'Избраният от Вас час се припокрива с друга поръчка. Моля, изберете свободен час от календара.')

        return requested_date

