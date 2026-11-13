from datetime import timedelta, datetime, time
from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, TemplateView
from core.choices.status_choices import StatusChoices
from core.emails.order_confirmation_email import send_order_confirmation_email
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
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
        requested_date = form.cleaned_data['requested_date']
        print(dict(self.request.POST.items()))

        if not selected_variants:
            form.add_error(None, "Моля, изберете поне една услуга от калкулатора.")
            return self.form_invalid(form)

        for variant, quantity in selected_variants.items():
            calculated_real_total_price += variant.price * quantity
            calculated_total_execution_time += variant.execution_time_in_minutes * quantity

        end_hour = requested_date + timedelta(minutes=calculated_total_execution_time)

        local_start = timezone.localtime(requested_date)
        local_end = timezone.localtime(end_hour)

        if local_end.date() > local_start.date() or local_end.time() > time(18, 30):
            form.add_error(
                None,
                "Вашата поръчка ще надхвърля максималното ни работно време (до 18:30). "
                "Моля, изберете по-ранен час или по-малко услуги."
            )
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.end_hour = end_hour

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

            context = {
                'full_name': self.object.full_name,
                'requested_date': self.object.requested_date,
                'user_email': self.object.email,
                'order_items': list(selected_variants.items()),
                'total_price': calculated_real_total_price,
                'has_discount': has_discount
            }

            transaction.on_commit(lambda: send_order_confirmation_email(
                context=context
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


class CalendarView(TemplateView):
    template_name = 'common/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            requested_date = parse_date(self.request.GET.get('selected_date', '') or '')
        except ValueError:
            requested_date = None

        if requested_date is None:
            requested_date = timezone.localdate()

        orders = Order.objects.filter(requested_date__date=requested_date).exclude(status=StatusChoices.DENIED).only('requested_date', 'end_hour')

        day_hours_slots = {
            '09:00':True,
            '09:30': True,
            '10:00': True,
            '10:30': True,
            '11:00': True,
            '11:30': True,
            '12:00': True,
            '12:30': True,
            '13:00': True,
            '13:30': True,
            '14:00': True,
            '14:30': True,
            '15:00': True,
            '15:30': True,
            '16:00': True,
            '16:30': True,
            '17:00': True,
            '17:30': True
        }


        for order in orders:
            start_hour = timezone.localtime(order.requested_date).time()
            end_hour = timezone.localtime(order.end_hour).time()

            for slot in day_hours_slots:
                curr_slot_time = datetime.strptime(slot, '%H:%M').time()
                if start_hour <= curr_slot_time < end_hour:
                    day_hours_slots[slot] = False

        context['day_hours_slots'] = day_hours_slots
        return context


