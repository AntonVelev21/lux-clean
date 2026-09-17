from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(requested_date, user_email, order_items):
    formated_date = requested_date.strftime("%d.%m.%Y")
    formated_time = requested_date.strftime("%H:%M")
    """
    To do:
    - Take order services and format them in the email message
    """
    subject = 'Потвърждение на вашата резервация'
    message = f'Здравейте! Вашата резервация за {order_items} на {formated_date} от {formated_time} часът беше успешна.'
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False
    )