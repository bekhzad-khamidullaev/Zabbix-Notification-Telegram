from django.contrib import admin
from .models import Dashboard, Widget


class WidgetInline(admin.TabularInline):
    model = Widget
    extra = 0


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    inlines = [WidgetInline]
    list_display = ('name', 'user')
