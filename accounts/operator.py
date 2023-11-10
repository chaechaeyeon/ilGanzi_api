from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .models import User
from .views import resetWatered



def start():
    scheduler=BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    @scheduler.scheduled_job('cron', hour=0, minute=22, name = 'resetWatered')
    def auto_resetWatered():
        resetWatered()
    scheduler.start()