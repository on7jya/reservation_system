import datetime
import random

from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.reservation.models import Reservation
from apps.rooms.models import Room, Office
from apps.users.models import Person


def random_string(length):
    """Возвращает идентификатор из 11 символов"""
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    chars_2 = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    return ''.join([random.choice(chars + chars_2) for i in range(0, length)])


def random_date(start):
    """Возвращает рандомную дату между start и start+1 час"""
    delta = datetime.timedelta(hours=1)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


class ReservationModelTest(TestCase):

    def setUp(self):
        """Тестовые данные"""
        for id_num in range(10, 100, 1):
            office = Office.objects.create(id=id_num, name=random_string(50))
            user = Person.objects.create(
                id=id_num, password=random_string(11),
                username=random_string(20),
                first_name=random_string(10), last_name=random_string(10),
                email=random_string(10), office=office
            )
            room = Room.objects.create(id=id_num, name=random_string(10), office=office, size=random.randint(1, 100),
                                       availability=True)

            tz = timezone.get_current_timezone()
            begin = tz.localize(datetime.datetime(2116, 6, 1, 8, 0, 0))
            reservation = Reservation.objects.create(id=id_num, room=room, created_by=user,
                                                     subject=random_string(50),
                                                     start_meeting_time=random_date(begin),
                                                     end_meeting_time=random_date(begin) + datetime.timedelta(hours=2))

    def _test_field_cannot_be_empty(self, field_name):
        reservation = Reservation()
        with self.assertRaises(ValidationError):
            Reservation._meta.get_field(field_name).clean(getattr(reservation, field_name), reservation)

    def test_room_cannot_be_empty(self):
        try:
            self._test_field_cannot_be_empty('room')
        except Reservation.room.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_created_by_cannot_be_empty(self):
        try:
            self._test_field_cannot_be_empty('created_by')
        except Reservation.created_by.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_subject_cannot_be_empty(self):
        try:
            self._test_field_cannot_be_empty('subject')
        except Reservation.subject.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_start_meeting_time_cannot_be_empty(self):
        try:
            self._test_field_cannot_be_empty('start_meeting_time')
        except Reservation.start_meeting_time.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_end_meeting_time_cannot_be_empty(self):
        try:
            self._test_field_cannot_be_empty('end_meeting_time')
        except Reservation.end_meeting_time.RelatedObjectDoesNotExist:
            self.assertTrue(True)
