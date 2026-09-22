from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(
    requested_date, user_email, order_items, total_price
):
    formatted_date = requested_date.strftime("%d.%m.%Y")
    formatted_time = requested_date.strftime("%H:%M")

    old_price = total_price * Decimal(str(1.05))
    old_price_str = f"{old_price:.2f}"
    total_price_str = f"{total_price:.2f}"

    subject = "Потвърждение на вашата резервация"

    text_order_info = "\n".join(
        f"- {item.service}: {item.quantity} бр" for item in order_items
    )
    plain_message = (
        f"Здравейте!\n\n"
        f"Вашата резервация за почистване на:\n{text_order_info}\n\n"
        f"Стара цена: {old_price_str} € -> Нова цена: {total_price_str} €\n"
        f"на {formatted_date} от {formatted_time} (*ориентировъчен час) беше успешна!\n\n"
        f"Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите."
    )

    html_order_info = "<br>".join(
        f"- {item.service}: {item.quantity} бр" for item in order_items
    )
    html_message = f"""
    <p>Здравейте!</p>
    <p>Вашата резервация за почистване на:<br>{html_order_info}</p>
    <p>Стара цена: <del>{old_price_str} €</del> &rarr; Нова цена: <b>{total_price_str} €</b></p>
    <p>на {formatted_date} от {formatted_time} <i>(*ориентировъчен час)</i> беше успешна!</p>
    <p>Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите.</p>
    """

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        html_message=html_message,
        fail_silently=False,
    )