from django.contrib import admin
from .models import DashboardNote, DashboardLog

admin.site.register(DashboardNote)
admin.site.register(DashboardLog)
