from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .views import resetWatered
from django.conf import settings


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    register_events(scheduler)

    scheduler.add_job(
        resetWatered,
        trigger=CronTrigger(hour="0", minute="00"),
        max_instances=1,
        name="resetWatered",
    )

    scheduler.start()