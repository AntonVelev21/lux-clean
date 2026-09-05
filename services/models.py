from django.core.validators import MinValueValidator
from django.db import models

from core.validators import ServiceImageResolutionValidator


class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='services/images', validators=[
        ServiceImageResolutionValidator()
    ])

    def __str__(self):
        return self.name


class ServiceVariant(models.Model):
    service = models.ForeignKey('Service', related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[
        MinValueValidator(0.00, message='Service price can not be negative.')
    ])
    execution_time_in_minutes = models.PositiveIntegerField()
    image = models.ImageField(upload_to='services/images')

    def __str__(self):
        return self.name