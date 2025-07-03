from django.urls import path, include

urlpatterns = [
    path('', include('monitor.urls')),
    path('api/v1/', include('webapp.api.urls')),
]
