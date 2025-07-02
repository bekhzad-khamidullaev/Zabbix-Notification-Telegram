from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from zbxTelegram import get_offline_hosts, get_zabbix_user


@csrf_exempt
def offline_hosts(request):
    tg_id = request.GET.get('telegram_id')
    if not tg_id or get_zabbix_user(tg_id) is None:
        return JsonResponse({'error': 'unauthorized'}, status=403)
    groups = request.GET.get('groups')
    hosts = get_offline_hosts(groups)
    return JsonResponse({'offline': hosts})
