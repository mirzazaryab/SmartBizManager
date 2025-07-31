from django import forms
from django.core.exceptions import ValidationError
from .models import Payment
from orders.models import Order

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'amount', 'payment_method', 'status']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = Order.objects.filter(status__in=['pending', 'under_processing'])

    def clean(self):
        cleaned_data = super().clean()
        order = cleaned_data.get('order')
        amount = cleaned_data.get('amount')
        if order and amount:
            paid_amount = sum(payment.amount for payment in Payment.objects.filter(order=order).exclude(id=self.instance.id))
            remaining_amount = order.total_price - paid_amount
            if amount > remaining_amount:
                raise ValidationError(f"Payment amount (Rs: {amount}) cannot exceed remaining amount (Rs: {remaining_amount}).")
        return cleaned_data