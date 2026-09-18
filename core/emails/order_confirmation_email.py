from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(requested_date, user_email, order_items, total_price):
    formated_date = requested_date.strftime("%d.%m.%Y")
    formated_time = requested_date.strftime("%H:%M")
    formated_order_info = '\n'.join(f"- {order_item.service}: {order_item.quantity} бр" for order_item in order_items)
    subject = 'Потвърждение на вашата резервация'
    message = (f'Здравейте! Вашата резервация за почистване на: \n{formated_order_info.lower()} \nС обща цена {total_price} €, на {formated_date} от {formated_time} *ориентировъчен час беше успешна!'
               f'\n Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите.')
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False
    )
