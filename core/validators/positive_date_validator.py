from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.deconstruct import deconstructible


"""
Removed from the model for now.
Validation for requested date is implemented in forms.py with clean_requested_date method.
"""

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