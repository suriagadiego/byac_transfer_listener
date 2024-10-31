import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bayc_event.settings")
app = Celery("bayc_event")

app.conf.CELERY_IMPORTS = ("web3_transaction.tasks",)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "polling-task-every-30-seconds": {
        "task": "web3_transaction.tasks.listen_for_events",
        "schedule": timedelta(seconds=30),
    },
    "polling-task-every-4pm-utc": {
        "task": "web3_transaction.tasks.catchup_events",
        "schedule": crontab(hour=16, minute=0),  # 4 PM UTC
    },
}
