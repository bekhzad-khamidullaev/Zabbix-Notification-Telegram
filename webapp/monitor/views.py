from django.http import JsonResponse
from zbxTelegram import get_offline_hosts


def offline_hosts(request):
    groups = request.GET.get('groups')
    hosts = get_offline_hosts(groups)
    return JsonResponse({'offline': hosts})
