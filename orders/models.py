from django.core.validators import MinValueValidator
from django.db import models
from core.choices.city_choices import CityChoices
from core.choices.status_choices import StatusChoices
from core.validators.client_phone_validator import ClientPhoneValidator


class Order(models.Model):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, validators=[
        ClientPhoneValidator()
    ])
    email = models.EmailField()
    city = models.CharField(max_length=30, choices=CityChoices.choices)
    address = models.TextField()
    requested_date = models.DateTimeField(null=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[
        MinValueValidator(0.00, 'The total order price cannot be negative.')
    ])
    end_hour = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=StatusChoices.choices, default=StatusChoices.NEW)

    def __str__(self):
        return f"Поръчка #{self.id} от {self.full_name}"



class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    service = models.ForeignKey('services.ServiceVariant', related_name='items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.service.name} (към Поръчка #{self.order.id})"