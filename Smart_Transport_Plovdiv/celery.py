import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Transport_Plovdiv.settings')


app = Celery('Smart_Transport_Plovdiv')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


