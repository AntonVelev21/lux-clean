import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from services.models import Service


class ServiceCreateMixin:
    @staticmethod
    def _create_image(width, height):
        file_obj = io.BytesIO()
        image = Image.new('RGB', (width, height), color='white')
        image.save(file_obj, format='JPEG')
        file_obj.seek(0)
        return SimpleUploadedFile(
            name='service_image.jpg',
            content=file_obj.read(),
            content_type='image/jpeg'
        )

    def _create_service(self, **kwargs):
        defaults = {
            'name': 'Пране на пердета',
            'description': 'Детайлно почистване и пране на пердета.',
            'image': self._create_image(1920, 800),
            'slug': None
        }

        defaults.update(kwargs)
        if not defaults['slug']:
            defaults.pop('slug')

        return Service.objects.create(**defaults)