import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'familyBudgetApp.settings')

app = Celery('familyBudgetApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
