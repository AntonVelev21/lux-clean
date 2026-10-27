import shutil
import tempfile
from django.test import TestCase, override_settings
from services.tests.mixins import ServiceCreateMixin

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ServiceDetailTests(ServiceCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_get_context_data_returns_correct_kvp(self):
        service = self._create_service()
        response = self.client.get(f'/services/{service.slug}/')
        context_data = {0: 'Пране', 1: 'на', 2: 'пердета'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['name_parts'], context_data)

