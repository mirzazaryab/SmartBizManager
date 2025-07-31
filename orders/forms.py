from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product_name', 'quantity', 'unit_price', 'notes', 'status']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'aria-label': 'Select customer',
                'required': True
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter product name',
                'aria-label': 'Product name',
                'required': True
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter quantity',
                'aria-label': 'Quantity',
                'min': 1,
                'required': True
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter unit price',
                'aria-label': 'Unit price',
                'min': 0.01,
                'step': 0.01,
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'rows': 3,
                'placeholder': 'Enter any additional notes (optional)',
                'aria-label': 'Order notes'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'aria-label': 'Select status',
                'required': True
            }),
        }