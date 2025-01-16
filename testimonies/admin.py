from django.contrib import admin
from .models import Testimony

# Register your models here.


class TestimonyAdmin(admin.ModelAdmin):
    list_display = ["full_name", "role", "show"]
    search_fields = ["full_name", "role"]
    list_filter = ["show"]


admin.site.register(Testimony, TestimonyAdmin)
