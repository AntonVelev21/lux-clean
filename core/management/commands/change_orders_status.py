from datetime import datetime

from django.core.management import BaseCommand

from core.choices.status_choices import StatusChoices
from orders.models import Order


class Command(BaseCommand):
    help = "Takes all orders for the current date from the database, and changes their status according to the current time."


    def handle(self, *args, **options):
        now = datetime.now()
        orders_for_the_day = Order.objects.filter(requested_date__date=now.date()).select_related('reserved_hours')
        changed_to_finished = 0
        changed_to_in_process = 0

        for order in orders_for_the_day:
            if now.hour > order.reserved_hours.end_hour.hour:
                order.status = StatusChoices.FINISHED
                order.save()
                changed_to_finished += 1

            else:
                in_process = False
                if now.hour >= order.reserved_hours.start_hour.hour:
                    if order.reserved_hours.end_hour.hour > now.hour:
                        in_process = True
                    elif order.reserved_hours.end_hour.hour == now.hour:
                        if order.reserved_hours.end_hour.minute >= now.minute:
                            in_process = True
                if in_process:
                    order.status = StatusChoices.IN_PROCESS
                    order.save()
                    changed_to_in_process += 1

        self.stdout.write(self.style.SUCCESS(f'Operation finished. {changed_to_finished} orders were changed to "FINISHED" '
                                             f'and {changed_to_in_process} orders were changed to "IN PROCESS"'))


