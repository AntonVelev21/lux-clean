from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import re

@deconstructible
class ClientPhoneValidator:
    def __init__(self, message=None):
        self.message = message


    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            value = "Enter a valid phone number."
        self.__message = value


    def __call__(self, number):
        pattern = r'^(?:\+?359|00359|0)\d{8,9}$'
        if not re.match(pattern, number):
            raise ValidationError(self.__message)


@deconstructible
class PositiveDateValidator:
    def __init__(self, message=None):
        self.message = message


    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            value = "You can not request a date in the past."
        self.__message = value

    def __call__(self, date_and_time):
        now = timezone.now()
        if date_and_time < now:
            raise ValidationError(self.__message)
