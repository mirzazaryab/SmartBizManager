from django.db import models

class DashboardNote(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DashboardLog(models.Model):
    action = models.CharField(max_length=255)
    performed_by = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.performed_by} - {self.action[:30]} ({self.timestamp.strftime('%Y-%m-%d')})"
