from django.contrib import admin
from services.models import Service, ServiceVariant


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    ...


@admin.register(ServiceVariant)
class ServiceVariantAdmin(admin.ModelAdmin):
    ...