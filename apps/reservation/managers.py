import datetime

import pytz
from django.db import models
from django.db.models import Q

from config import settings

DEFAULT_TZ = pytz.timezone(settings.TIME_ZONE)


class ReservationManager(models.Manager):
    def pending(self):
        return self.filter(state="0")

    def accepted(self):
        return self.filter(state="1")

    def canceled(self):
        return self.filter(state="2")

    def overlaps(self, begin, end):
        qs = Q(begin__lt=end) & Q(end__gt=begin)
        return self.filter(qs)

    def for_date(self, date, interval_days):
        if isinstance(date, str):
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            assert isinstance(date, datetime.date)
        dt = datetime.datetime.combine(date, datetime.datetime.min.time())
        start_dt = DEFAULT_TZ.localize(dt)
        end_dt = start_dt + datetime.timedelta(days=interval_days)
        return self.overlaps(start_dt, end_dt)
