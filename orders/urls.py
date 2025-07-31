from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.order_create, name='order_add'),
    path('<int:pk>/edit/', views.order_update, name='order_edit'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
]
