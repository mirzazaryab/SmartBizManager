from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm

# 🔍 View All Customers
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'customers/customer_list.html', {'customers': customers})

# ➕ Add New Customer
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully.')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add Customer'})

# ✏️ Update Existing Customer
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Update Customer'})

# ❌ Delete Customer
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_delete_confirm.html', {'customer': customer})

# 📄 View Customer Detail
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})
