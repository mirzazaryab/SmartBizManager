from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'payment_method', 'timestamp']
    list_filter = ['payment_method', 'timestamp']
    search_fields = ['order__id']
