from django.contrib import admin
from .models import ErrorLog

# Register your models here.


class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ["app_name", "traceback", "timestamp", "severity"]
    list_filter = ["app_name", "timestamp", "severity"]


admin.site.register(ErrorLog, ErrorLogAdmin)
