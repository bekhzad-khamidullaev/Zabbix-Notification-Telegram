from django.contrib import admin
from django.forms import PasswordInput
from .models import ZabbixConnectionSettings


@admin.register(ZabbixConnectionSettings)
class ZabbixConnectionSettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ZabbixConnectionSettings._meta.get_field('service_account_password'): {
            'widget': PasswordInput()
        }
    }

    def has_add_permission(self, request):
        return not ZabbixConnectionSettings.objects.exists()
