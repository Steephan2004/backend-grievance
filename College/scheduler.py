# College/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore


from .views import updateDataEmail

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

def start_scheduler():
    scheduler.add_job(
        updateDataEmail,
        trigger=CronTrigger(day_of_week="mon", hour="09", minute="00"),
        id="weekly_report",
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()

def shutdown_scheduler():
    scheduler.shutdown()
