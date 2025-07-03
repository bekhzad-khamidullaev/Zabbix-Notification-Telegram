import hashlib
import json
from urllib.parse import urljoin
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
import requests
from ..configuration.models import ZabbixConnectionSettings
from ..accounts.models import User
from ..dashboard.models import Dashboard, Widget
from ..alerts.models import CustomAlertRule
from ..notifications.models import WebPushSubscription
from ..integrations.models import IntegrationSettings
from ..utils.models import AuditLog
from .serializers import (
    DashboardSerializer,
    WidgetSerializer,
    CustomAlertRuleSerializer,
    WebPushSubscriptionSerializer,
    IntegrationSettingsSerializer,
    AuditLogSerializer,
    UserSerializer,
)
from .mixins import AuditLogMixin


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            cfg = ZabbixConnectionSettings.objects.get(is_active=True)
        except ZabbixConnectionSettings.DoesNotExist:
            return Response({'error': 'Service unavailable'}, status=503)
        payload = {
            'jsonrpc': '2.0',
            'method': 'user.login',
            'params': {'user': username, 'password': password},
            'id': 1,
        }
        try:
            resp = requests.post(urljoin(cfg.zabbix_api_url, 'api_jsonrpc.php'), json=payload, verify=False)
            data = resp.json()
            token = data.get('result')
        except Exception:
            token = None
        if not token:
            return Response({'error': 'Invalid credentials'}, status=401)
        user, _ = User.objects.get_or_create(username=username)
        AuditLog.objects.create(user=user, action='login', details={'user': username})
        refresh = RefreshToken.for_user(user)
        jti = str(refresh.access_token['jti'])
        cache.set(f'zabbix_token:{user.id}:{jti}', token, cfg.cache_ttl_seconds)
        return Response({'access_token': str(refresh.access_token), 'refresh_token': str(refresh)})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        jti = request.auth['jti']
        key = f'zabbix_token:{request.user.id}:{jti}'
        token = cache.get(key)
        if token:
            cfg = ZabbixConnectionSettings.objects.filter(is_active=True).first()
            if cfg:
                payload = {
                    'jsonrpc': '2.0',
                    'method': 'user.logout',
                    'params': [],
                    'auth': token,
                    'id': 1,
                }
                try:
                    requests.post(urljoin(cfg.zabbix_api_url, 'api_jsonrpc.php'), json=payload, verify=False)
                except Exception:
                    pass
        cache.delete(key)
        AuditLog.objects.create(user=request.user, action='logout', details={})
        return Response(status=204)


class ZabbixProxyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        body = request.data
        jti = request.auth['jti']
        key = f'zabbix_token:{request.user.id}:{jti}'
        token = cache.get(key)
        if not token:
            return Response({'error': 'Unauthorized'}, status=401)
        cfg = ZabbixConnectionSettings.objects.filter(is_active=True).first()
        if not cfg:
            return Response({'error': 'Service unavailable'}, status=503)
        cache_key = hashlib.sha256((str(request.user.id)+json.dumps(body, sort_keys=True)).encode()).hexdigest()
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        body['auth'] = token
        try:
            resp = requests.post(urljoin(cfg.zabbix_api_url, 'api_jsonrpc.php'), json=body, verify=False)
            data = resp.json()
        except Exception:
            return Response({'error': 'Upstream error'}, status=502)
        cache.set(cache_key, data, cfg.cache_ttl_seconds)
        AuditLog.objects.create(user=request.user, action='zabbix_proxy', details={'method': body.get('method')})
        return Response(data)


class DashboardViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Dashboard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        self.log_action(instance, 'create')

    def perform_update(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'update')

    def perform_destroy(self, instance):
        self.log_action(instance, 'delete')
        super().perform_destroy(instance)


class WidgetViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Widget.objects.filter(dashboard__user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'create')

    def perform_update(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'update')

    def perform_destroy(self, instance):
        self.log_action(instance, 'delete')
        super().perform_destroy(instance)


class CustomAlertRuleViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = CustomAlertRuleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = CustomAlertRule.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'create')

    def perform_update(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'update')

    def perform_destroy(self, instance):
        self.log_action(instance, 'delete')
        super().perform_destroy(instance)


class WebPushSubscriptionViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = WebPushSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return WebPushSubscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        self.log_action(instance, 'create')

    def perform_update(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'update')

    def perform_destroy(self, instance):
        self.log_action(instance, 'delete')
        super().perform_destroy(instance)


class IntegrationSettingsViewSet(AuditLogMixin, viewsets.ModelViewSet):
    serializer_class = IntegrationSettingsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = IntegrationSettings.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'create')

    def perform_update(self, serializer):
        instance = serializer.save()
        self.log_action(instance, 'update')

    def perform_destroy(self, instance):
        self.log_action(instance, 'delete')
        super().perform_destroy(instance)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return AuditLog.objects.filter(user=self.request.user)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        AuditLog.objects.create(
            user=request.user,
            action="profile.update",
            details=serializer.validated_data,
        )
        return Response(serializer.data)
