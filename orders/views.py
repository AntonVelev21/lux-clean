from django.db import transaction
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from orders.forms import OrderCreateForm
from orders.models import Order, OrderItem
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

            self.object.total_price = calculated_real_total_price
            self.object.total_execution_time_in_minutes = calculated_total_execution_time
            self.object.save(update_fields=['total_price', 'total_execution_time_in_minutes'])

        return HttpResponseRedirect(self.get_success_url())




def get_available_days_for_order(request: HttpRequest) -> HttpResponse:
    ...
