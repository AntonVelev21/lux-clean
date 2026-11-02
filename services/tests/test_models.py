import shutil
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.test.utils import override_settings
from services.tests.mixins import ServiceCreateMixin, TEMP_MEDIA_ROOT



@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ServiceModelTests(ServiceCreateMixin, TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


    def test_service_with_invalid_image_resolution_fails_validation_and_raises_exception(self):
        service_with_invalid_image_size = self.create_service(image=self._create_image(100, 100))
        expected_error_message = f'You can not save service image with size 100x100 px.\n'f'Image should be at least 1920x800 px.'
        with self.assertRaises(ValidationError) as context:
            service_with_invalid_image_size.full_clean()

        self.assertEqual(context.exception.messages[0], expected_error_message)

    def test_service_with_valid_image_resolution_passes_validation(self):
        service = self.create_service()
        try:
            service.full_clean()

        except ValidationError:
            self.fail('Validation failed during full_clean()! Service with valid image resolution does not pass validation!')


    def test_service_slug_with_only_valid_letters_creates_successfully(self):
        service = self.create_service()
        self.assertEqual(service.slug, 'prane-na-perdeta')


    def test_save_method_does_not_overwrite_manually_set_slugs(self):
        service = self.create_service(slug='prane-na-perdeta-manually_set')
        self.assertEqual(service.slug, 'prane-na-perdeta-manually_set')

