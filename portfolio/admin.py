from django.contrib import admin
from .models import Portfolio

# Register your models here.


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


admin.site.register(Portfolio, PortfolioAdmin)
