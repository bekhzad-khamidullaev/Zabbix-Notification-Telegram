from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(
        max_length=10,
        choices=[('admin', 'Admin'), ('operator', 'Operator'), ('viewer', 'Viewer')],
        default='viewer'
    )
    telegram_chat_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.password:
            self.set_unusable_password()
        super().save(*args, **kwargs)
