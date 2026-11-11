from django.db.models.signals import post_save
from django.dispatch import receiver
from core.choices.status_choices import StatusChoices
from orders.models import Order


@receiver(post_save, sender=Order)
def delete_reserved_hours_for_denied_order(instance: Order, created, **kwargs):
    if not created:
        if instance.status == StatusChoices.DENIED:
            instance.requested_date, instance.end_hour = None, None
            instance.save()







