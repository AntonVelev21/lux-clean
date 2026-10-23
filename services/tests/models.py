import io
from unittest import TestCase
import os
import django
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cleaners_bg.settings')
django.setup()

from services.models import Service
from PIL import Image

"""
Create Service instance
Test:
- ServiceImageResolutionValidator
- slug generation in save() method
"""
class ServiceModelTests(TestCase):
    def setUp(self):
        file_obj = io.BytesIO()
        image  = Image.new('RGB', (100, 100), color='white')
        image.save(file_obj, format='JPEG')
        file_obj.seek(0)
        invalid_image = SimpleUploadedFile(
            name='image_with_invalid_size.jpg',
            content=file_obj.read(),
            content_type='image/jpeg'
        )

        self.service_with_invalid_size_image = Service.objects.create(
            name='Пране на пердета',
            description='Детайлно почистване, пране и изушаване на пердета.',
            image=invalid_image
        )

    def test_service_with_invalid_size_image_raises_exception(self):
        with self.assertRaises(ValidationError) as context:
            self.service_with_invalid_size_image.full_clean()

        self.assertEqual(context.exception.messages[0],f'You can not save service image with size 100x100 px.\n'
                                                   f'Image should be at least 1920x800 px.')