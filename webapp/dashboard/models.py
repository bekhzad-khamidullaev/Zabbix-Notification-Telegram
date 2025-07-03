from django.db import models
from django.conf import settings


class Dashboard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grid_layout = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Widget(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    widget_type = models.CharField(max_length=50)
    config = models.JSONField(default=dict)
    position = models.JSONField()

    def __str__(self):
        return f'{self.widget_type} on {self.dashboard.name}'
