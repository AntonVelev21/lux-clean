from django.forms.models import ModelForm

from orders.models import Order


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['created_at', 'updated_at', 'status', 'total_price']