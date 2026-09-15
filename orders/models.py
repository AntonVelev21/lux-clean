from django.core.validators import MinValueValidator
from django.db import models

from core.choices import CityChoices, StatusChoices
from core.validators import ClientPhoneValidator, PositiveDateValidator


class Order(models.Model):
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, validators=[
        ClientPhoneValidator()
    ])
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=30, choices=CityChoices.choices)
    address = models.TextField()
    requested_date = models.DateTimeField(validators=[
        PositiveDateValidator()
    ])
    total_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[
        MinValueValidator(0.00, 'The total order price cannot be negative.')
    ])
    total_execution_time_in_minutes = models.PositiveIntegerField()
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



class ReservedHours(models.Model):
    order = models.OneToOneField('Order', related_name='reserved_hours', on_delete=models.CASCADE)
    start_hour = models.DateTimeField()
    end_hour = models.DateTimeField()