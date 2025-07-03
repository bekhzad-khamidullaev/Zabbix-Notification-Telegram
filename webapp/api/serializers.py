from rest_framework import serializers
from ..dashboard.models import Dashboard, Widget
from ..alerts.models import CustomAlertRule
from ..notifications.models import WebPushSubscription
from ..integrations.models import IntegrationSettings
from ..utils.models import AuditLog
from ..accounts.models import User


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'dashboard', 'widget_type', 'config', 'position']


class DashboardSerializer(serializers.ModelSerializer):
    widgets = WidgetSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = ['id', 'user', 'name', 'grid_layout', 'widgets']


class CustomAlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAlertRule
        fields = ['id', 'name', 'conditions', 'actions', 'is_active', 'cooldown_seconds']


class WebPushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebPushSubscription
        fields = ['id', 'user', 'subscription_data', 'user_agent']


class IntegrationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationSettings
        fields = ['id', 'integration_type', 'settings', 'is_enabled']


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'details', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'telegram_chat_id']
        read_only_fields = ['username', 'role']
