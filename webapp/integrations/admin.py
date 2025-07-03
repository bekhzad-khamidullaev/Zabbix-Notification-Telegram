from django.contrib import admin
from .models import IntegrationSettings


@admin.register(IntegrationSettings)
class IntegrationSettingsAdmin(admin.ModelAdmin):
    list_display = ('integration_type', 'is_enabled')
    list_filter = ('integration_type', 'is_enabled')
