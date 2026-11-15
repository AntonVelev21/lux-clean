from django.utils import timezone
from django.core.management import BaseCommand
from core.choices.status_choices import StatusChoices
from orders.models import Order


class Command(BaseCommand):
    help = "Takes all orders for the current date from the database, and changes their status according to the current time."


    def handle(self, *args, **options):
        now = timezone.localtime()
        updatable = [StatusChoices.NEW, StatusChoices.IN_PROCESS]
        orders_for_the_day = Order.objects.filter(status__in=updatable)
        finished = 0
        in_process = 0

        for order in orders_for_the_day:
            start = timezone.localtime(order.requested_date)
            end = timezone.localtime(order.end_hour)

            if now >= end:
                new_status = StatusChoices.FINISHED
            elif now >= start:
                new_status = StatusChoices.IN_PROCESS
            else:
                continue

            if order.status != new_status:
                order.status = new_status
                order.save(update_fields=["status"])
                if new_status == StatusChoices.FINISHED:
                    finished += 1
                else:
                    in_process += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. {finished} orders -> "FINISHED", {in_process} orders -> "IN PROCESS".'
        ))


