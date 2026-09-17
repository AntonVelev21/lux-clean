from django.db.models.signals import post_save
from django.dispatch import receiver

from core.choices.status_choices import StatusChoices
from orders.models import Order, ReservedHours


@receiver(post_save, sender=Order)
def delete_reserved_hours_for_denied_order(instance: Order, created, **kwargs):
    if not created:
        if instance.status == StatusChoices.DENIED:
            try:
                instance.reserved_hours.delete()

            except ReservedHours.DoesNotExist:
                pass


