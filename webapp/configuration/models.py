from django.db import models
from django_cryptography.fields import encrypt


class ZabbixConnectionSettings(models.Model):
    zabbix_api_url = models.URLField(unique=True)
    service_account_user = models.CharField(max_length=128, blank=True, null=True)
    service_account_password = encrypt(models.CharField(max_length=255))
    is_active = models.BooleanField(default=True)
    cache_ttl_seconds = models.PositiveIntegerField(default=60)

    def save(self, *args, **kwargs):
        if not self.pk and ZabbixConnectionSettings.objects.exists():
            raise ValueError('Only one ZabbixConnectionSettings instance is allowed')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.zabbix_api_url
