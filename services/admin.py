from django.contrib import admin
from .models import Service

# Register your models here.


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "service_type", "description"]
    search_fields = ["name", "service_type"]
    list_filter = ["service_type"]


admin.site.register(Service, ServiceAdmin)
