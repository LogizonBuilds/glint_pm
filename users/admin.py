from django.contrib import admin
from .models import User, Setting

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "date_joined", "last_login", "is_active", "is_staff"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["email"]


admin.site.register(User, UserAdmin)
admin.site.register(Setting)
