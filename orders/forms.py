from django.forms.models import ModelForm


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
            'address': 'Вашият адрес'
        }