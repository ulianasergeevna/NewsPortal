import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal', include=['News_Portal.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
