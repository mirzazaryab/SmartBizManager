# customer_order_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard/')),
    path('dashboard/', include('dashboard.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('customers/', include('customers.urls')),
    # path('invoices/', include('invoices.urls')),
]

