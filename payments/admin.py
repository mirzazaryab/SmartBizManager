# payments/admin.py
from django.contrib import admin
from .models import Payment  # Changed from Payments to Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order__product_name', 'order__customer__name']