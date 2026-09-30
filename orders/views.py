from datetime import timedelta
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from core.emails.order_confirmation_email import send_order_confirmation_email
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem, ReservedHours
from services.models import Service, ServiceVariant


class CreateOrderView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:confirmation')


    def _get_selected_variants(self):
        selected = {}

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
                        selected[variant] = quantity

                    except ServiceVariant.DoesNotExist:
                        continue
        return selected


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.prefetch_related('variants').all()
        variant_id = self.request.GET.get('variant_id')
        try:
            variant = ServiceVariant.objects.get(id=variant_id)
            context['requested_variant'] = variant

        except ServiceVariant.DoesNotExist:
            context['requested_variant'] = None

        if self.request.method == 'POST':
            context['selected_variants'] = self._get_selected_variants()
        else:
            context['selected_variants'] = None

        return context


    def form_valid(self, form):
        calculated_real_total_price = 0
        calculated_total_execution_time = 0
        has_discount = False
        selected_variants = self._get_selected_variants()

        if not selected_variants:
            form.add_error(None, "Моля, изберете поне една услуга от калкулатора.")
            return self.form_invalid(form)

        for variant, quantity in selected_variants.items():
            calculated_real_total_price += variant.price * quantity
            calculated_total_execution_time += variant.execution_time_in_minutes * quantity

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.total_execution_time_in_minutes = calculated_total_execution_time

            if calculated_real_total_price >= 200:
                price_after_discount = calculated_real_total_price * Decimal(str(0.95))
                has_discount = True

            if has_discount:
                self.object.total_price = price_after_discount
                total_price_text_for_confirmation_template = f'{price_after_discount:.2f}'
            else:
                self.object.total_price = calculated_real_total_price
                total_price_text_for_confirmation_template = f'{calculated_real_total_price:.2f}'
            self.object.save()

            for variant, quantity in selected_variants.items():
                OrderItem.objects.create(
                    order=self.object,
                    service=variant,
                    quantity=quantity
                )

            end_hour = self.object.requested_date + timedelta(hours=calculated_total_execution_time / 60)
            ReservedHours.objects.create(
                order_id=self.object.id,
                start_hour=self.object.requested_date,
                end_hour=end_hour
            )

            transaction.on_commit(lambda: send_order_confirmation_email(
                requested_date=self.object.requested_date,
                user_email=self.object.email,
                order_items=list(selected_variants.items()),
                total_price=calculated_real_total_price,
                has_discount=has_discount
            ))

            self.request.session['order_confirmation'] = {
                'full_name': self.object.full_name,
                'email': self.object.email,
                'phone_number': self.object.phone_number,
                'formatted_date': self.object.requested_date.strftime('%d.%m.%Y'),
                'formatted_time': self.object.requested_date.strftime('%H:%M'),
                'total_price': total_price_text_for_confirmation_template,
                'has_discount': has_discount,
                'old_price': f'{calculated_real_total_price:.2f}',
            }

        return HttpResponseRedirect(self.get_success_url())



class OrderConfirmationView(TemplateView):
    template_name = 'orders/confirmation.html'

    def get(self, request, *args, **kwargs):
        confirmation = request.session.pop('order_confirmation', None)
        if not confirmation:
            return HttpResponseRedirect(reverse('home-page'))
        return self.render_to_response({'order': confirmation})



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


