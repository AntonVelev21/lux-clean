import shutil
from tkinter.font import names

from django.test import TestCase, override_settings
from django.urls.base import reverse

from services.tests.mixins import ServiceCreateMixin, TEMP_MEDIA_ROOT


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ServiceViewTests(ServiceCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_get_context_data_in_detail_view_returns_correct_kvp(self):
        service = self._create_service(name='Пране на пердета')
        url = reverse('services:detail', kwargs={'slug': service.slug})
        response = self.client.get(url)
        context_data = {0: 'Пране', 1: 'на', 2: 'пердета'}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['name_parts'], context_data)


    def test_detail_view_not_found(self):
        url = reverse('services:detail', kwargs={'slug': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_list_services_expect_success(self):
        service = self._create_service(name='Пране на пердета')
        url = reverse('services:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(service, response.context['object_list'])


    def test_list_services_empty_state(self):
        url = reverse('services:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
