from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('add/', views.payment_add, name='payment_add'),
    path('<int:pk>/edit/', views.edit_payment, name='edit_payment'),
    path('<int:pk>/delete/', views.delete_payment, name='delete_payment'),
    path('<int:payment_id>/', views.payment_details, name='payment_details'),
]