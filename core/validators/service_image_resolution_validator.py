from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible


@deconstructible
class ServiceImageResolutionValidator:
    width_required = 1920
    height_required = 800

    def __init__(self, message=None):
        self.message = message


    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            value = (
                f'You can not save service image with size %(width)sx%(height)s px.\n'
                f'Image should be at least {self.width_required}x{self.height_required} px.'
            )
        self.__message = value


    def __call__(self, image):
        width, height = get_image_dimensions(image)
        if width < self.width_required or height < self.height_required:
            raise ValidationError(message=self.__message,
                                  params={
                                      'width': width,
                                      'height': height
                                  })