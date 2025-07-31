from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import Payment
from decimal import Decimal
from django.db.models import Sum
@login_required(login_url='login')
def payment_add(request):
    form = PaymentForm(request.POST or None)
    order_totals = {}
    advance_payments = {}
    last_payment_dates = {}
    remaining_amounts = {}

    try:
        if not form.fields['order'].queryset.exists():
            messages.warning(request, 'No orders available. Please create an order first.')
        for order in form.fields['order'].queryset:
            order_id = str(order.id)
            order_totals[order_id] = str(order.total_price)
            payments = Payment.objects.filter(order=order)
            total_advance = sum(payment.amount for payment in payments)
            advance_payments[order_id] = str(total_advance)
            last_payment = payments.order_by('-created_at').first()
            last_payment_dates[order_id] = str(last_payment.created_at.date()) if last_payment else ''
            remaining_amounts[order_id] = str(max(Decimal('0.00'), order.total_price - total_advance))
        print('order_totals:', order_totals)
        print('advance_payments:', advance_payments)
        print('last_payment_dates:', last_payment_dates)
        print('remaining_amounts:', remaining_amounts)
    except Exception as e:
        print('Error generating payment data:', str(e))
        messages.error(request, f'Error loading payment data: {str(e)}')

    if request.method == 'POST' and form.is_valid():
        payment = form.save(commit=False)
        order = payment.order
        total_advance = sum(p.amount for p in Payment.objects.filter(order=order))
        remaining = order.total_price - total_advance
        if payment.amount > remaining:
            messages.error(request, f'Payment amount ({payment.amount}) exceeds remaining balance ({remaining}).')
            return render(request, 'payments/add_payment.html', {
                'form': form,
                'order_totals': order_totals,
                'advance_payments': advance_payments,
                'last_payment_dates': last_payment_dates,
                'remaining_amounts': remaining_amounts
            })
        payment.save()
        messages.success(request, f'Payment of Rs: {payment.amount} for Order name "{order.customer.name}" has been added ')
        return redirect('payments:payment_list')
    elif request.method == 'POST':
        messages.error(request, 'Error adding payment. Please check the form.')

    return render(request, 'payments/add_payment.html', {
        'form': form,
        'order_totals': order_totals,
        'advance_payments': advance_payments,
        'last_payment_dates': last_payment_dates,
        'remaining_amounts': remaining_amounts
    })

@login_required(login_url='login')
def payment_list(request):
    payments = Payment.objects.select_related('order__customer').order_by('-created_at')
    paid_amounts = {
        order_id: total or 0
        for order_id, total in Payment.objects.values('order_id').annotate(total=Sum('amount')).values_list('order_id', 'total')
    }
    for payment in payments:
        payment.paid_amount = paid_amounts.get(payment.order_id, 0)
        payment.remaining_amount = payment.order.total_price - payment.paid_amount
    return render(request, 'payments/payment_list.html', {'payments': payments})

def edit_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payments:payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payments/payment_form.html', {'form': form})

def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return redirect('payments:payment_list')
    return render(request, 'payments/delete_payment.html', {'payment': payment})

def payment_details(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    paid_amount = Payment.objects.filter(order_id=payment.order_id).aggregate(total=Sum('amount'))['total'] or 0
    remaining_amount = payment.order.total_price - paid_amount
    return render(request, 'payments/payment_details.html', {
        'payment': payment,
        'paid_amount': paid_amount,
        'remaining_amount': remaining_amount
    })