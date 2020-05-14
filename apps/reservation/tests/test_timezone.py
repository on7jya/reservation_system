import datetime

import pytest
from django.test import TestCase
from django.utils.timesince import timesince, timeuntil
from django.utils.timezone import FixedOffset
from pytz.reference import LocalTimezone

pytestmark = pytest.mark.django_db


class TimeZoneTest(TestCase):

    def setUp(self):
        self.t = datetime.datetime(2020, 5, 10, 13, 46, 0)
        self.onemicrosecond = datetime.timedelta(microseconds=1)
        self.onesecond = datetime.timedelta(seconds=1)
        self.oneminute = datetime.timedelta(minutes=1)
        self.onehour = datetime.timedelta(hours=1)
        self.oneday = datetime.timedelta(days=1)
        self.oneweek = datetime.timedelta(days=7)
        self.onemonth = datetime.timedelta(days=30)
        self.oneyear = datetime.timedelta(days=365)

    def test_equal_datetimes(self):
        """ equal datetimes. """
        # NOTE: \xa0 avoids wrapping between value and unit
        self.assertEqual(timesince(self.t, self.t), '0\xa0минут')

    def test_ignore_microseconds_and_seconds(self):
        """ Microseconds and seconds are ignored. """
        self.assertEqual(timesince(self.t, self.t + self.onemicrosecond),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t + self.onesecond),
                         '0\xa0минут')

    def test_other_units(self):
        """ Test other units. """
        self.assertEqual(timesince(self.t, self.t + self.oneminute),
                         '1\xa0минута')
        self.assertEqual(timesince(self.t, self.t + self.onehour), '1\xa0час')
        self.assertEqual(timesince(self.t, self.t + self.oneday), '1\xa0день')
        self.assertEqual(timesince(self.t, self.t + self.oneweek), '1\xa0неделя')
        self.assertEqual(timesince(self.t, self.t + self.onemonth), '1\xa0месяц')
        self.assertEqual(timesince(self.t, self.t + self.oneyear), '1\xa0год')

    def test_multiple_units(self):
        """ Test multiple units. """
        self.assertEqual(timesince(self.t,
                                   self.t + 2 * self.oneday + 6 * self.onehour), '2\xa0дня, 6\xa0часов')
        self.assertEqual(timesince(self.t,
                                   self.t + 2 * self.oneweek + 2 * self.oneday), '2\xa0недели, 2\xa0дня')

    def test_display_first_unit(self):
        """
        If the two differing units aren't adjacent, only the first unit is
        displayed.
        """
        self.assertEqual(timesince(self.t,
                                   self.t + 2 * self.oneweek + 3 * self.onehour + 4 * self.oneminute),
                         '2\xa0недели')

        self.assertEqual(timesince(self.t,
                                   self.t + 4 * self.oneday + 5 * self.oneminute), '4\xa0дня')

    def test_display_second_before_first(self):
        """
        When the second date occurs before the first, we should always
        get 0 minutes.
        """
        self.assertEqual(timesince(self.t, self.t - self.onemicrosecond),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.onesecond),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.oneminute),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.onehour),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.oneday),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.oneweek),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.onemonth),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t, self.t - self.oneyear),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t,
                                   self.t - 2 * self.oneday - 6 * self.onehour), '0\xa0минут')
        self.assertEqual(timesince(self.t,
                                   self.t - 2 * self.oneweek - 2 * self.oneday), '0\xa0минут')
        self.assertEqual(timesince(self.t,
                                   self.t - 2 * self.oneweek - 3 * self.onehour - 4 * self.oneminute),
                         '0\xa0минут')
        self.assertEqual(timesince(self.t,
                                   self.t - 4 * self.oneday - 5 * self.oneminute), '0\xa0минут')

    def test_different_timezones(self):
        """ Тестируем две различные таймзоны """
        now = datetime.datetime.now()
        now_tz = datetime.datetime.now(LocalTimezone(now))
        now_tz_i = datetime.datetime.now(FixedOffset((3 * 60) + 15))

        self.assertEqual(timesince(now), f'0\xa0минут')
        self.assertEqual(timesince(now_tz), "0\xa0минут")
        self.assertEqual(timeuntil(now_tz, now_tz_i), "0\xa0минут")

    def test_date_objects(self):
        """ Both timesince and timeuntil should work on date objects (#17937). """
        today = datetime.date.today()
        self.assertEqual(timesince(today + self.oneday), '0\xa0минут')
        self.assertEqual(timeuntil(today - self.oneday), '0\xa0минут')

    def test_both_date_objects(self):
        """ Timesince should work with both date objects (#9672) """
        today = datetime.date.today()
        self.assertEqual(timeuntil(today + self.oneday, today), '1\xa0день')
        self.assertEqual(timeuntil(today - self.oneday, today), '0\xa0минут')
        self.assertEqual(timeuntil(today + self.oneweek, today), '1\xa0неделя')

    def test_naive_datetime_with_tzinfo_attribute(self):
        class Naive(datetime.tzinfo):
            def utcoffset(self, dt):
                return None

        future = datetime.datetime(2080, 1, 1, tzinfo=Naive())
        self.assertEqual(timesince(future), '0\xa0минут')
        past = datetime.datetime(1980, 1, 1, tzinfo=Naive())
        self.assertEqual(timeuntil(past), '0\xa0минут')
