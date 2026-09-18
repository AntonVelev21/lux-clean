import json
from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpRequest
from django.utils import timezone

from core.choices.status_choices import StatusChoices

STATUS_ORDER = [
    StatusChoices.NEW,
    StatusChoices.IN_PROCESS,
    StatusChoices.FINISHED,
    StatusChoices.DENIED,
]

# Fixed, non-themed status colors so the meaning of a color never
# changes with the admin's light/dark theme or brand color.
STATUS_COLORS = {
    StatusChoices.NEW: "#2a78d6",
    StatusChoices.IN_PROCESS: "#fab219",
    StatusChoices.FINISHED: "#0ca30c",
    StatusChoices.DENIED: "#d03b3b",
}

TREND_WINDOW_DAYS = 14


def new_orders_badge(request: HttpRequest) -> str:
    from orders.models import Order

    return str(Order.objects.filter(status=StatusChoices.NEW).count())


def _money(value: Decimal | None) -> Decimal:
    return value if value is not None else Decimal("0.00")


def _format_delta(current: float, previous: float) -> dict[str, Any] | None:
    if not previous:
        return None

    change = (current - previous) / previous * 100
    return {"value": f"{abs(change):.1f}%", "positive": change >= 0}


def dashboard_callback(request: HttpRequest, context: dict[str, Any]) -> dict[str, Any]:
    from orders.models import Order, OrderItem

    today = timezone.localdate()
    period_start = today - timedelta(days=TREND_WINDOW_DAYS - 1)
    previous_period_start = period_start - timedelta(days=TREND_WINDOW_DAYS)

    orders_qs = Order.objects.all()

    total_orders = orders_qs.count()
    total_revenue = _money(orders_qs.aggregate(total=Sum("total_price"))["total"])
    avg_order_value = _money(orders_qs.aggregate(avg=Avg("total_price"))["avg"])
    new_orders = orders_qs.filter(status=StatusChoices.NEW).count()

    current_period = orders_qs.filter(created_at__date__gte=period_start)
    previous_period = orders_qs.filter(
        created_at__date__gte=previous_period_start,
        created_at__date__lt=period_start,
    )

    current_period_revenue = float(_money(current_period.aggregate(total=Sum("total_price"))["total"]))
    previous_period_revenue = float(_money(previous_period.aggregate(total=Sum("total_price"))["total"]))
    current_period_count = current_period.count()
    previous_period_count = previous_period.count()

    daily_rows = {
        row["day"]: row
        for row in (
            current_period
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(revenue=Sum("total_price"), orders=Count("id"))
        )
    }

    labels = []
    revenue_series = []
    for offset in range(TREND_WINDOW_DAYS):
        day = period_start + timedelta(days=offset)
        labels.append(day.strftime("%b %d"))
        row = daily_rows.get(day)
        revenue_series.append(float(row["revenue"]) if row and row["revenue"] else 0)

    revenue_chart = {
        "labels": labels,
        "datasets": [
            {
                "label": "Revenue (BGN)",
                "data": revenue_series,
                "borderColor": "var(--color-primary-500)",
                "backgroundColor": "var(--color-primary-500)",
                "fill": False,
                "tension": 0.35,
            }
        ],
    }

    counts_by_status = {
        row["status"]: row["count"]
        for row in orders_qs.values("status").annotate(count=Count("id"))
    }
    status_labels = dict(StatusChoices.choices)

    status_chart = {
        "labels": [status_labels[status] for status in STATUS_ORDER],
        "datasets": [
            {
                "label": "Orders",
                "data": [counts_by_status.get(status, 0) for status in STATUS_ORDER],
                "backgroundColor": [STATUS_COLORS[status] for status in STATUS_ORDER],
                "maxTicksXLimit": len(STATUS_ORDER),
            }
        ],
    }

    top_services = (
        OrderItem.objects
        .values("service__name")
        .annotate(total_qty=Sum("quantity"))
        .order_by("-total_qty")[:5]
    )

    context.update({
        "kpi_cards": [
            {
                "title": "Total revenue",
                "value": f"{total_revenue:,.2f} BGN",
                "icon": "payments",
                "delta": _format_delta(current_period_revenue, previous_period_revenue),
            },
            {
                "title": "Total orders",
                "value": total_orders,
                "icon": "receipt_long",
                "delta": _format_delta(current_period_count, previous_period_count),
            },
            {
                "title": "New / pending orders",
                "value": new_orders,
                "icon": "pending_actions",
                "delta": None,
            },
            {
                "title": "Average order value",
                "value": f"{avg_order_value:,.2f} BGN",
                "icon": "point_of_sale",
                "delta": None,
            },
        ],
        "revenue_chart": json.dumps(revenue_chart),
        "status_chart": json.dumps(status_chart),
        "top_services": top_services,
        "recent_orders": orders_qs.order_by("-created_at")[:6],
        "trend_window_days": TREND_WINDOW_DAYS,
    })

    return context
