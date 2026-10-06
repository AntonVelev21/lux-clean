from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_confirmation_email(context):
    full_name = context['full_name']
    requested_date = context['requested_date']
    user_email = context['user_email']
    order_items = context['order_items']
    total_price = context['total_price']
    has_discount = context['has_discount']

    template_name = 'emails/email-confirmation.html'
    formatted_date = requested_date.strftime("%d.%m.%Y")
    formatted_time = requested_date.strftime("%H:%M")
    total_price_str = f"{total_price:.2f}"
    text_order_info = "\n".join(
        f"- {service}: {quantity} бр" for service, quantity in order_items
    )

    if has_discount:
        price_after_discount = total_price * Decimal(str(0.95))
        price_after_discount_str = f"{price_after_discount:.2f}"
        price_info_text = f"Стара цена: {total_price_str} € -> Цена с приложена 5% отстъпка: {price_after_discount_str} €\n"
        context['price_after_discount'] = price_after_discount
    else:
        price_info_text = f"С цена: {total_price_str} €\n"

    subject = "Потвърждение на вашата резервация"
    plain_message = (
        f"Здравейте, {full_name}!\n\n"
        f"Вашата резервация за почистване на:\n{text_order_info}\n\n"
        f"{price_info_text}"
        f"на {formatted_date} от {formatted_time} (*ориентировъчен час) беше успешна!\n\n"
        f"Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите."
    )

    html = render_to_string(template_name, context)

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        html_message=html,
        fail_silently=False,
    )
