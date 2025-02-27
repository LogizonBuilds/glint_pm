from django.contrib import admin
from .models import User, Setting, Transaction

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "date_joined", "last_login", "is_active", "is_staff"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["email"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "amount",
        "transaction_reference",
        "transaction_date",
        "service_name",
        "transaction_status",
    ]
    list_filter = [
        "service_name",
        "transaction_status",
        "transaction_date",
        "transaction_currency",
    ]
    search_fields = ["user__email", "transaction_reference"]
    readonly_fields = ["transaction_reference"]


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Setting)
