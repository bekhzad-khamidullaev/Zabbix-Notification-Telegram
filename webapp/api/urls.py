from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    LogoutView,
    ZabbixProxyView,
    DashboardViewSet,
    WidgetViewSet,
    CustomAlertRuleViewSet,
    WebPushSubscriptionViewSet,
    IntegrationSettingsViewSet,
    AuditLogViewSet,
    ProfileView,
)

router = DefaultRouter()
router.register('dashboards', DashboardViewSet, basename='dashboard')
router.register('widgets', WidgetViewSet, basename='widget')
router.register('alert-rules', CustomAlertRuleViewSet, basename='alert-rule')
router.register('push-subscriptions', WebPushSubscriptionViewSet, basename='push-subscription')
router.register('integrations', IntegrationSettingsViewSet, basename='integration')
router.register('audit-logs', AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/profile/', ProfileView.as_view()),
    path('zabbix/', ZabbixProxyView.as_view()),
]

urlpatterns += router.urls
