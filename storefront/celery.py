
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

celery = Celery('storefront')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
# now we need to load this module inside the __init__ module of the current package,
# coz otherwise python is not gonna execute this code
