from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'telegram_chat_id')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'telegram_chat_id'),
        }),
    )
    readonly_fields = [f.name for f in User._meta.fields if f.name != 'role']
    list_display = ('username', 'role', 'telegram_chat_id')
    ordering = ('username',)
