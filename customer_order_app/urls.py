# customer_order_app/urls.py
from accounts.views import login_view
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('dashboard/', include('dashboard.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('customers/', include('customers.urls')),
    path('accounts/', include('accounts.urls')),
]

