from django.contrib import admin
from django.utils.html import format_html

from unfold.admin import ModelAdmin, TabularInline

from services.models import Service, ServiceVariant


class ServiceVariantInline(TabularInline):
    model = ServiceVariant
    extra = 0
    fields = ["name", "price", "execution_time_in_minutes", "image", "thumbnail"]
    readonly_fields = ["thumbnail"]

    def thumbnail(self, obj):
        if not obj.pk or not obj.image:
            return "—"
        return format_html(
            '<img src="{}" class="h-12 w-12 rounded-default object-cover" />',
            obj.image.url,
        )

    thumbnail.short_description = "Preview"


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["name", "thumbnail", "variant_count", "description_preview"]
    search_fields = ["name", "description"]
    inlines = [ServiceVariantInline]
    exclude = ['slug']

    def thumbnail(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" class="h-10 w-10 rounded-default object-cover" />',
            obj.image.url,
        )

    thumbnail.short_description = "Image"

    def variant_count(self, obj):
        return obj.variants.count()

    variant_count.short_description = "Variants"

    def description_preview(self, obj):
        return format_html(
            '<span class="text-font-subtle-light dark:text-font-subtle-dark">{}</span>',
            (obj.description[:80] + "…") if len(obj.description) > 80 else obj.description,
        )

    description_preview.short_description = "Description"


@admin.register(ServiceVariant)
class ServiceVariantAdmin(ModelAdmin):
    list_display = ["name", "service", "thumbnail", "price", "execution_time_in_minutes"]
    list_filter = ["service"]
    search_fields = ["name", "service__name"]
    autocomplete_fields = ["service"]

    def thumbnail(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" class="h-10 w-10 rounded-default object-cover" />',
            obj.image.url,
        )

    thumbnail.short_description = "Image"
