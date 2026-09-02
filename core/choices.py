from django.db import models


class CityChoices(models.TextChoices):
    SOFIA = 'sofia', 'Sofia'


class StatusChoices(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROCESS = 'in_process', 'In process'
    FINISHED = 'finished', 'Finished'
    DENIED = 'denied', 'Denied'
