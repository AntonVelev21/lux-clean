from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from core.validators.service_image_resolution_validator import ServiceImageResolutionValidator


BG_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
    'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
    'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sht', 'ъ': 'a',
    'ь': 'y', 'ю': 'yu', 'я': 'ya',
}

class Service(models.Model):
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='services/images', validators=[
        ServiceImageResolutionValidator()
    ])


    def save(self, *args, **kwargs):
        if not self.slug:
            name_for_slug = ''.join(BG_MAP[l.lower()] if l.lower() in BG_MAP else l.lower() for l in self.name)
            self.slug = slugify(name_for_slug)
            super().save(*args, **kwargs)

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