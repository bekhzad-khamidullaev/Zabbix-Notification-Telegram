from django.db import models
from django_cryptography.fields import encrypt


class IntegrationSettings(models.Model):
    INTEGRATION_CHOICES = [
        ('slack', 'Slack'),
        ('webhook', 'Webhook'),
    ]
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_CHOICES)
    settings = encrypt(models.JSONField())
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.integration_type
