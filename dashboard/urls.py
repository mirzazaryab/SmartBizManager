from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_overview, name='overview'),
    path('charts/', views.charts, name='charts'),
]
