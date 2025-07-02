from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = 'dummy'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'monitor',
]
MIDDLEWARE = ['django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'webapp.urls'
TEMPLATES = []
WSGI_APPLICATION = 'webapp.wsgi.application'
