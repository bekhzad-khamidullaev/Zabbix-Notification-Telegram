from django.db import models
from django.conf import settings


class WebPushSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription_data = models.JSONField()
    user_agent = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} subscription'
