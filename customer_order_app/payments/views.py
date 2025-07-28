from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from orders.models import Order
from customers.models import Customer
from .forms import PaymentForm

def payment_list(request):
    payments = Payment.objects.select_related('order__customer').order_by('-timestamp')
    return render(request, 'payments/payment_list.html', {'payments': payments})

def payment_add(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment:list')
    else:
        form = PaymentForm()
    return render(request, 'payment/payment_form.html', {'form': form})

def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment:list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payment/payment_form.html', {'form': form})

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('payment:list')
    return render(request, 'payment/payment_confirm_delete.html', {'payment': payment})
