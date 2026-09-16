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
            'requested_date': 'Вижте свободните дати и часове'
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_time_field = self.fields['requested_date']
        date_time_field.widget.input_type = 'datetime-local'



    def clean_requested_date(self):
        now = timezone.now()
        if self.cleaned_data.get('requested_date') < now:
            raise ValidationError("You can not request a date in the past.")