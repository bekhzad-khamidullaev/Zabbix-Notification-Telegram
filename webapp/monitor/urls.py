from django.urls import path
from . import views

urlpatterns = [
    path('offline/', views.offline_hosts, name='offline_hosts'),
]
