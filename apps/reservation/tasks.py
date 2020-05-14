# Create your tasks here
from __future__ import absolute_import, unicode_literals

from datetime import timedelta, datetime

from celery import Celery
from celery.task import periodic_task
from celery.utils.time import LocalTimezone

from config.settings import AUTO_CANCEL_INTERVAL

celery = Celery('tasks', broker='amqp://guest@localhost//')  # !


@periodic_task(run_every=timedelta(seconds=60))
def auto_cancel_reservation():
    from apps.reservation.models import Reservation
    now_tz = datetime.now(LocalTimezone())
    for reservation in Reservation.objects.all():
        if reservation.state == '0' and now_tz > reservation.start_meeting_time + timedelta(
                minutes=AUTO_CANCEL_INTERVAL):
            Reservation.auto_cancel(reservation)
            reservation.save()
