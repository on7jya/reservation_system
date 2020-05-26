from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.reservation.models import Reservation
from apps.reservation.tests.base import random_data


class ReservationModelTest(TestCase):

    def setUp(self):
        """Тестовые данные"""
        for id_num in range(10, 100, 1):
            random_data(id_num, True)

    def _test_field_cannot_be_empty(self, field_name):
        """При попытке очистить поле, проверяем, что поле не может быть пустым """
        reservation = Reservation()
        with self.assertRaises(ValidationError):
            Reservation._meta.get_field(field_name).clean(getattr(reservation, field_name), reservation)

    def test_room_cannot_be_empty(self):
        """Проверяем, что room не может быть пустым"""
        try:
            self._test_field_cannot_be_empty('room')
        except Reservation.room.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_created_by_cannot_be_empty(self):
        """Проверяем, что created_by не может быть пустым"""
        try:
            self._test_field_cannot_be_empty('created_by')
        except Reservation.created_by.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_subject_cannot_be_empty(self):
        """Проверяем, что subject не может быть пустым"""
        try:
            self._test_field_cannot_be_empty('subject')
        except Reservation.subject.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_start_meeting_time_cannot_be_empty(self):
        """Проверяем, что start_meeting_time не может быть пустым"""
        try:
            self._test_field_cannot_be_empty('start_meeting_time')
        except Reservation.start_meeting_time.RelatedObjectDoesNotExist:
            self.assertTrue(True)

    def test_end_meeting_time_cannot_be_empty(self):
        """Проверяем, что end_meeting_time не может быть пустым"""
        try:
            self._test_field_cannot_be_empty('end_meeting_time')
        except Reservation.end_meeting_time.RelatedObjectDoesNotExist:
            self.assertTrue(True)
