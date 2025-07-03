from urllib.parse import urljoin
import requests
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.conf import settings
from webapp.configuration.models import ZabbixConnectionSettings
from webapp.accounts.models import User


def _send_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.tg_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    kwargs = {"timeout": 5}
    if settings.tg_proxy:
        kwargs["proxies"] = settings.tg_proxy_server
    try:
        requests.post(url, data=data, **kwargs)
    except Exception:
        pass


def _notify_users(event):
    message = f"Zabbix event {event.get('eventid')}"
    name = event.get('name')
    if name:
        message += f": {name}"
    chat_ids = User.objects.exclude(telegram_chat_id__isnull=True).values_list(
        "telegram_chat_id", flat=True
    )
    for chat_id in chat_ids:
        if chat_id:
            _send_telegram(chat_id, message)


@shared_task
def poll_zabbix_events():
    cfg = ZabbixConnectionSettings.objects.filter(is_active=True).first()
    if not cfg:
        return

    token = cache.get('service_zabbix_token')
    if not token:
        payload = {
            'jsonrpc': '2.0',
            'method': 'user.login',
            'params': {
                'user': cfg.service_account_user,
                'password': cfg.service_account_password,
            },
            'id': 1,
        }
        try:
            resp = requests.post(urljoin(cfg.zabbix_api_url, 'api_jsonrpc.php'), json=payload, verify=False)
            token = resp.json().get('result')
            if token:
                cache.set('service_zabbix_token', token, cfg.cache_ttl_seconds)
        except Exception:
            return

    last_time = cache.get('zabbix_last_event_ts', 0)
    payload = {
        'jsonrpc': '2.0',
        'method': 'event.get',
        'params': {
            'output': 'extend',
            'time_from': last_time + 1,
        },
        'auth': token,
        'id': 1,
    }
    try:
        resp = requests.post(urljoin(cfg.zabbix_api_url, 'api_jsonrpc.php'), json=payload, verify=False)
        events = resp.json().get('result', [])
    except Exception:
        return

    if not events:
        return

    last_ts = max(int(e.get('clock', last_time)) for e in events)
    cache.set('zabbix_last_event_ts', last_ts)

    channel_layer = get_channel_layer()
    for event in events:
        event_type = 'problem' if event.get('value') == '1' else 'update'
        async_to_sync(channel_layer.group_send)(
            'problems',
            {'type': 'send.update', 'data': {'event': event, 'event_type': event_type}},
        )
        _notify_users(event)
