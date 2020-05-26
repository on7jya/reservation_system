from django.test import TestCase

from apps.reservation.api.serializers import ReservationSerializer
from apps.reservation.models import Reservation
from apps.reservation.tests.base import random_data


class ReservationModelTest(TestCase):

    def setUp(self):
        """Тестовые данные"""
        for id_num in range(10, 100, 1):
            random_data(id_num, False)

    def test_start_date_should_be_before_end_date(self):
        """Проверяем, что начальная дата не может быть больше конечной"""
        for id_num in range(10, 100, 1):
            serializer = ReservationSerializer(instance=Reservation(id_num))
            serializer = ReservationSerializer(data=serializer.data)
            self.assertFalse(serializer.is_valid())
            self.assertIn('end_meeting_time', serializer.errors)
