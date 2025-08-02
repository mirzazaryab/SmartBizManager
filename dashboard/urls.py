from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_overview, name='overview'),
    path('charts/', views.charts, name='charts'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('expenses/', views.view_expenses, name='view_expenses'),
    path('expenses/edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]
