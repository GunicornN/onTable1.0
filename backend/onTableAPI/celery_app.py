##
# CELERY : Creation of Worker
## 
import os

from celery import Celery
from django.conf import settings

"""
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onTableAPI.settings.common')

app = Celery(settings.CELERY_NAME,broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BACKEND)

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onTableAPI.settings.common')
 
app = Celery('onTableAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')