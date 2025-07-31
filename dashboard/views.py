from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncWeek
from orders.models import Order
from customers.models import Customer
from payments.models import Payment
from datetime import datetime, timedelta
import logging
from django.utils import timezone

# Set up logging
logger = logging.getLogger(__name__)

@never_cache
@login_required(login_url='accounts:login')
def dashboard_overview(request):
    # Ensure timezone is set to PKT
    timezone.activate('Asia/Karachi')

    # Card data with case-insensitive filtering
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status__iexact='pending').count()
    delivered_orders = Order.objects.filter(status__iexact='delivered').count()

    # Debug logging for cards
    logger.debug(f"Total Customers: {total_customers}")
    logger.debug(f"Total Orders: {total_orders}")
    logger.debug(f"Pending Orders: {pending_orders}")
    logger.debug(f"Delivered Orders: {delivered_orders}")
    logger.debug(f"Order statuses: {list(Order.objects.values_list('status', flat=True).distinct())}")
    logger.debug(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    cards = [
        {
            "title": "Total Customers",
            "count": total_customers,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "icon": "bi-person",
            "css_class": "customers"
        },
        {
            "title": "Total Orders",
            "count": total_orders,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "icon": "bi-cart",
            "css_class": "orders"
        },
        {
            "title": "Pending Orders",
            "count": pending_orders,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "icon": "bi-hourglass-split",
            "css_class": "pending"
        },
        {
            "title": "Delivered Orders",
            "count": delivered_orders,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "icon": "bi-check-circle",
            "css_class": "delivered"
        },
    ]

    # Line chart: Weekly sales (unit_price * quantity)
    weekly_sales = (Order.objects
        .filter(unit_price__isnull=False, quantity__isnull=False)  # Ensure non-null fields
        .annotate(
            week=TruncWeek('created_at'),
            total=ExpressionWrapper(
                F('unit_price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
        .values('week')
        .annotate(total_sales=Sum('total'))
        .order_by('week'))

    # Generate fallback data for the last 12 weeks if empty
    if not weekly_sales:
        logger.debug("No weekly sales data found, generating fallback data")
        today = timezone.now().date()
        chart_labels = [(today - timedelta(weeks=i)).strftime('%b %d, %Y') for i in range(11, -1, -1)]
        chart_data = [0.0] * 12
    else:
        weekly_sales = weekly_sales[:12]  # Limit to last 12 weeks
        chart_labels = [sale['week'].strftime('%b %d, %Y') for sale in weekly_sales]
        chart_data = [float(sale['total_sales'] or 0) for sale in weekly_sales]
        logger.debug(f"Weekly sales: {list(weekly_sales)}")

    # Bar chart: Order management (total orders vs. pending orders)
    order_management = {
        'total_orders': total_orders,
        'pending_orders': pending_orders
    }
    order_labels = ['Total Orders', 'Pending Orders']
    order_data = [order_management['total_orders'], order_management['pending_orders']]

    # Transactions: Recent payments
    transactions = Payment.objects.select_related('order__customer').order_by('-created_at')[:10]

    return render(request, "dashboard/overview.html", {
        "cards": cards,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "order_labels": order_labels,
        "order_data": order_data,
        "transactions": transactions,
    })

def sales_report(request):
    sales = Order.objects.all().order_by('-created_at')
    return render(request, "dashboard/sales_report.html", {
        "sales": sales
    })

def pending_orders(request):
    orders = Order.objects.filter(status__iexact="pending").order_by('-created_at')
    return render(request, "dashboard/pending_orders.html", {
        "pending_orders": orders
    })

def delivered_orders(request):
    orders = Order.objects.filter(status__iexact="delivered").order_by('-created_at')
    return render(request, "dashboard/delivered_orders.html", {
        "delivered_orders": orders
    })

def charts(request):
    labels = ['Jan', 'Feb', 'Mar', 'Apr']
    values = [100, 200, 150, 300]
    return render(request, 'dashboard/charts.html', {
        'labels': labels,
        'values': values,
    })