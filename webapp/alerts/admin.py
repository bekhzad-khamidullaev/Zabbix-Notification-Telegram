from django.contrib import admin
from .models import CustomAlertRule


@admin.register(CustomAlertRule)
class CustomAlertRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
