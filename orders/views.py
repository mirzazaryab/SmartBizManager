from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from django.contrib import messages
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()  # Save the form and get the order instance
            messages.success(request, f'Order for "{order.product_name}" was successfully added!')
            return redirect('payments:payment_add')
        else:
            messages.error(request, 'Error adding order. Please check the form.')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders:order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        product_name = order.product_name
        order.delete()
        messages.success(request, f'Order "{product_name}" was successfully deleted!')
        return redirect('orders:order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})