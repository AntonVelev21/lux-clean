from datetime import timedelta
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from core.emails.order_confirmation_email import send_order_confirmation_email
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem, ReservedHours
from services.models import Service, ServiceVariant


class CreateOrderView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('home-page')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.prefetch_related('variants').all()
        variant_id = self.request.GET.get('variant_id')
        try:
            variant = ServiceVariant.objects.get(id=variant_id)
            context['requested_variant'] = variant

        except ServiceVariant.DoesNotExist:
            context['requested_variant'] = None

        return context


    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.total_price = 0
            self.object.total_execution_time_in_minutes = 0
            self.object.save()
            calculated_real_total_price = 0
            calculated_total_execution_time = 0
            has_valid_services = False

            for key, value in self.request.POST.items():
                if key.startswith('variant_'):
                    try:
                        variant_id = key.split('_')[1]
                        quantity = int(value)
                    except (ValueError, IndexError):
                        continue

                    if quantity > 0:
                        try:
                            variant = ServiceVariant.objects.get(id=variant_id)
                            OrderItem.objects.create(
                                order=self.object,
                                service=variant,
                                quantity=quantity
                            )
                            calculated_real_total_price += quantity * variant.price
                            calculated_total_execution_time += quantity * variant.execution_time_in_minutes
                            has_valid_services = True

                        except ServiceVariant.DoesNotExist:
                            continue

            if not has_valid_services:
                transaction.set_rollback(True)
                form.instance.pk = None
                form.add_error(None, "Моля, изберете поне една услуга от калкулатора.")
                return self.form_invalid(form)

            if calculated_real_total_price >= 200:
                calculated_real_total_price -= calculated_real_total_price * Decimal(str(0.05))

            self.object.total_price = calculated_real_total_price
            self.object.total_execution_time_in_minutes = calculated_total_execution_time
            self.object.save(update_fields=['total_price', 'total_execution_time_in_minutes'])

            end_hour = self.object.requested_date + timedelta(hours=calculated_total_execution_time / 60)
            ReservedHours.objects.create(
                order_id=self.object.id,
                start_hour=self.object.requested_date,
                end_hour=end_hour
            )

            send_order_confirmation_email(requested_date=self.object.requested_date, user_email=self.object.email, order_items=self.object.items.all(), total_price=calculated_real_total_price)
        return HttpResponseRedirect(self.get_success_url())



class CalendarView(ListView):
    template_name = 'common/calendar.html'
    model = ReservedHours

    def get_context_data(self, **kwargs):
        context = super().get_context_data(object_list=self.get_queryset(), **kwargs)
        requested_date = self.request.GET.get('selected_date')
        reserved_hours = ReservedHours.objects.filter(start_hour__date=requested_date)
        day_hours_slots = {
            10: True,
            10.30: True,
            11: True,
            11.30: True,
            12: True,
            12.30: True,
            13: True,
            13.30: True,
            14: True,
            14.30: True,
            15: True,
            15.30: True,
            16: True,
            16.30: True

        }

        for time_slot in reserved_hours:
            day_hours_slots[time_slot.start_hour.hour] = False
            for hour in day_hours_slots:
                if hour <= time_slot.end_hour.hour:
                    day_hours_slots[hour] = False

        context['day_hours_slots'] = day_hours_slots
        return context


