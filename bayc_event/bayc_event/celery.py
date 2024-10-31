import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bayc_event.settings')
app = Celery('bayc_event')

app.conf.CELERY_IMPORTS = ('web3_transaction.tasks',)
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'polling-task-every-10-seconds': {
        'task': 'web3_transaction.tasks.listen_for_events',
        'schedule': timedelta(seconds=20),
    },
}