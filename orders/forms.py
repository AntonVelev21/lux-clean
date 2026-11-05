from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils import timezone

from orders.models import Order, ReservedHours


class OrderCreateForm(ModelForm):
    FIRST_WORKING_HOUR = 9
    LAST_WORKING_HOUR = 17
    VALID_HOURS = {00, 30}

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
        reserved_hours_for_the_day = ReservedHours.objects.filter(start_hour__date=requested_date)


        if requested_date < now:
            raise ValidationError('Моля изберете бъдещи час и дата.')


        if requested_date.hour > self.LAST_WORKING_HOUR:
            raise ValidationError('Избраният от Вас час не е в работното ни време. Моля, изберете час преди 17:00.')


        if requested_date.hour < self.FIRST_WORKING_HOUR:
            raise ValidationError('Избраният от Вас час не е в работното ни време. Моля, изберете час след 9:00.')


        if requested_date.minute not in self.VALID_HOURS:
            raise ValidationError('Избраният от Вас час не е валиден час за поръчка. Моля, изберете час завършващ на 00 или 30.')


        for time_slot in reserved_hours_for_the_day:
            if time_slot.start_hour.hour <= requested_date.hour < time_slot.end_hour.hour:
                raise ValidationError('Избраният от Вас час се припокрива с друга поръчка. Моля, изберете свободен час от календара.')


        return requested_date


