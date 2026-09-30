from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(requested_date, user_email, order_items, total_price, has_discount):
    formatted_date = requested_date.strftime("%d.%m.%Y")
    formatted_time = requested_date.strftime("%H:%M")
    total_price_str = f"{total_price:.2f}"
    html_order_info = "<br>".join(
        f"- {service}: {quantity} бр" for service, quantity in order_items
    )
    text_order_info = "\n".join(
        f"- {service}: {quantity} бр" for service, quantity in order_items
    )

    if has_discount:
        price_after_discount = total_price * Decimal(str(0.95))
        price_after_discount_str = f"{price_after_discount:.2f}"
        price_info_text = f"Стара цена: {total_price_str} € -> Цена с приложена 5% отстъпка: {price_after_discount_str} €\n"
        html_message = f"""
            <p>Здравейте!</p>
            <p>Вашата резервация за почистване на:<br>{html_order_info}</p>
            <p>Стара цена: <del>{total_price_str} €</del> &rarr; Цена с приложена 5% отстъпка: <b>{price_after_discount_str} €</b></p>
            <p>на {formatted_date} от {formatted_time} <i>(*ориентировъчен час)</i> беше успешна!</p>
            <p>Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите.</p>
            """
    else:
        price_info_text = f"С цена: {total_price_str} €\n"
        html_message = f"""
            <p>Здравейте!</p>
            <p>Вашата резервация за почистване на:<br>{html_order_info}</p>
            <p>С цена: <b>{total_price_str} €</b></p>
            <p>на {formatted_date} от {formatted_time} <i>(*ориентировъчен час)</i> беше успешна!</p>
            <p>Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите.</p>
            """


    subject = "Потвърждение на вашата резервация"

    plain_message = (
        f"Здравейте!\n\n"
        f"Вашата резервация за почистване на:\n{text_order_info}\n\n"
        f"{price_info_text}"
        f"на {formatted_date} от {formatted_time} (*ориентировъчен час) беше успешна!\n\n"
        f"Ще се свържем допълнително с вас за потвърждение и уточняване на детайлите."
    )


    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        html_message=html_message,
        fail_silently=False,
    )