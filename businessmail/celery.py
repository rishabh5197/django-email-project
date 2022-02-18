from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'businessmail.settings')

app = Celery('businessmail')
app.conf.enable_utc = False
app.conf.update(timezone='Indian/Mauritius')
app.config_from_object(settings, namespace='CELERY')


# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    'send_mail_daily': {
        'task': 'mails.task.schedulemail',
        'schedule': crontab(),
        # 'args': ('to', 'cc', 'bcc', 'title', 'description', 'attachment')
        # 'schedule': crontab(hour=16, minute=31, day_of_month=20, month_of_year=6,),
        # crontab is used for scheduling...
        # 'args':()
        # args are used for arguments....
        # task
    },
    'send_daily_mails': {
        'task': 'mails.task.dailymails',
        'schedule': crontab(),
    },
    'send_weekly_mails': {
        'task': 'mails.task.weekmails',
        'schedule': crontab(),
    },
    'send_monthly_mails': {
        'task': 'mails.task.monthmails',
        'schedule': crontab(),
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request:{self.request}")
