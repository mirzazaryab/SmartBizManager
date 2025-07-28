from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='list'),
    path('add/', views.payment_add, name='add'),
    path('<int:pk>/edit/', views.payment_edit, name='edit'),
    path('<int:pk>/delete/', views.payment_delete, name='delete'),
]
