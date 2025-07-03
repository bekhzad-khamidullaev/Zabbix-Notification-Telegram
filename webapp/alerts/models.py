from django.db import models
from django.conf import settings


class CustomAlertRule(models.Model):
    name = models.CharField(max_length=100)
    conditions = models.JSONField()
    actions = models.JSONField()
    is_active = models.BooleanField(default=True)
    cooldown_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
