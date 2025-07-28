from django.shortcuts import render
from datetime import datetime
from orders.models import Order
from customers.models import Customer

def dashboard_overview(request):
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    delivered_orders = Order.objects.filter(status='Delivered').count()

    cards = [
        {"title": "Total Customers", "count": total_customers},
        {"title": "Total Orders", "count": total_orders},
        {"title": "Pending Orders", "count": pending_orders},
        {"title": "Delivered Orders", "count": delivered_orders},
    ]

    # Dummy monthly chart data
    chart_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    chart_data = [30000, 25000, 40000, 32000, 28000, 45000]

    return render(request, "dashboard/overview.html", {
        "cards": cards,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    })

def sales_report(request):
    sales = Order.objects.all().order_by('-created_at')
    return render(request, "dashboard/sales_report.html", {
        "sales": sales
    })

def pending_orders(request):
    orders = Order.objects.filter(status="Pending").order_by('-created_at')
    return render(request, "dashboard/pending_orders.html", {
        "pending_orders": orders
    })

def delivered_orders(request):
    orders = Order.objects.filter(status="Delivered").order_by('-created_at')
    return render(request, "dashboard/delivered_orders.html", {
        "delivered_orders": orders
    })

def charts(request):
    # Dummy data for now
    labels = ['Jan', 'Feb', 'Mar', 'Apr']
    values = [100, 200, 150, 300]
    return render(request, 'dashboard/charts.html', {
        'labels': labels,
        'values': values,
    })

