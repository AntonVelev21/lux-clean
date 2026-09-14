from django import template

register = template.Library()


@register.filter
def format_hour(value):
    try:
        hour = int(value)
        minutes = round((float(value) - hour) * 100)
    except (TypeError, ValueError):
        return value

    return f"{hour:02d}:{minutes:02d}"
