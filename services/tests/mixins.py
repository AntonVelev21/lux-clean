import io
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from services.models import Service, ServiceVariant

TEMP_MEDIA_ROOT = tempfile.mkdtemp()

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


    def create_service(self, **kwargs):
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


    def create_service_variant(self, **kwargs):
        defaults = {
            'service': self.create_service(),
            'name': 'Голямо перде',
            'price': 30,
            'execution_time_in_minutes': 60,
            'image': self._create_image(1920, 800)
        }
        defaults.update(kwargs)

        return ServiceVariant.objects.create(**defaults)