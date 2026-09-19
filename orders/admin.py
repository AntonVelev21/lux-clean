from django.contrib import admin
from django.utils.html import format_html

from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RangeDateFilter
from unfold.decorators import display

from orders.models import Order, OrderItem, ReservedHours

STATUS_LABELS = {
    "new": "info",
    "in_process": "warning",
    "finished": "success",
    "denied": "danger",
}


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    tab = True
    autocomplete_fields = ["service"]


class ReservedHoursInline(TabularInline):
    model = ReservedHours
    extra = 0
    max_num = 1
    tab = True


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "phone_number",
        "city",
        "status_badge",
        "requested_date",
        "formatted_total_price",
        "created_at",
    ]

    ordering = ['-requested_date']

    list_display_links = ["id", "full_name"]

    list_filter = [
        ("status", ChoicesDropdownFilter),
        ("city", ChoicesDropdownFilter),
    ]
    list_filter_submit = True
    list_fullwidth = True
    search_fields = ["=id", "full_name", "phone_number", "email", "address"]
    date_hierarchy = "requested_date"
    readonly_fields = ["created_at", "updated_at"]
    actions = ["mark_as_in_process", "mark_as_finished", "mark_as_denied"]
    inlines = [OrderItemInline, ReservedHoursInline]

    fieldsets = (
        ("Client", {
            "fields": ("full_name", "phone_number", "email", "city", "address"),
        }),
        ("Order details", {
            "fields": ("status", "requested_date", "total_price", "total_execution_time_in_minutes"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @display(description="Status", label=STATUS_LABELS, ordering="status")
    def status_badge(self, obj):
        return obj.status, obj.get_status_display()

    @display(description="Total price", ordering="total_price")
    def formatted_total_price(self, obj):
        return format_html("{} €", obj.total_price)

    @admin.action(description="Mark selected orders as in process")
    def mark_as_in_process(self, request, queryset):
        queryset.update(status="in_process")

    @admin.action(description="Mark selected orders as finished")
    def mark_as_finished(self, request, queryset):
        queryset.update(status="finished")

    @admin.action(description="Mark selected orders as denied")
    def mark_as_denied(self, request, queryset):
        queryset.update(status="denied")


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ["order", "service", "quantity"]
    search_fields = ["=order__id", "order__full_name", "service__name"]
    autocomplete_fields = ["service"]


@admin.register(ReservedHours)
class ReservedHoursAdmin(ModelAdmin):
    list_display = ["order", "start_hour", "end_hour"]
    search_fields = ["=order__id", "order__full_name"]
