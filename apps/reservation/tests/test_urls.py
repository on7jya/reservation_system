import datetime
import json
import random
from datetime import timedelta

from django.db.models import F
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.reservation.api.serializers import ReservationSerializer
from apps.rooms.models import Room, Office
from apps.users.models import Person
from apps.reservation.models import Reservation

valid_request = {
    "created_by": "10",
    "room": "10",
    "subject": "Повестка встречи",
    "start_meeting_time": "2020-05-06T16:42:20.880Z",
    "end_meeting_time": "2020-05-06T18:42:20.881Z",
    "state": "0",
    "state_canceled": "0"
}

invalid_request = {
    "created_by": "1",
    "subject": "Повестка встречи",
    "start_meeting_time": "2021-05-06T16:42:20.880Z",
    "end_meeting_time": "",
    "state": "0",
    "state_canceled": "0"
}


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


class TestUrlsHttpResponse(TestCase):

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

    def test_get_reservation_list(self):
        """Тест - получение полного списка бронирований"""
        resp = self.client.get(reverse('reservation:reservation-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'application/json')

    def test_get_reservation_today_list(self):
        """Тест получения полного списка бронирований на день вперед"""
        resp = self.client.get(reverse('reservation:reservation-today-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'application/json')

    def test_get_reservation_room_today_list(self):
        """Тест получения списка бронирования переговорной {id} на день вперед """
        resp = self.client.get(reverse('reservation:reservation-room-today-list', args=[1, ]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['content-type'], 'application/json')

    def test_get_reservation_detail(self):
        """Тест получения информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.get(reverse('reservation:reservation-detail', args=[id_num, ]))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_put_reservation_detail(self):
        """Тест изменения информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.put(reverse('reservation:reservation-detail', args=[id_num, ]),
                                   data=json.dumps(valid_request),
                                   content_type='application/json',
                                   )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_patch_reservation_detail(self):
        """Тест частичного изменения информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.patch(reverse('reservation:reservation-detail', args=[id_num, ]),
                                     data=json.dumps(valid_request),
                                     content_type='application/json',
                                     )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_delete_reservation_detail(self):
        """Тест удаления информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.delete(reverse('reservation:reservation-detail', args=[id_num, ]))
            self.assertEqual(resp.status_code, 204)
            # A successful response SHOULD be 200 (OK) if the response includes an entity describing the status,
        # 202 (Accepted) if the action has not yet been enacted,
        # or 204 (No Content) if the action has been enacted but the response does not include an entity.

    def test_post_create_valid_reservation(self):
        """Тест создания бронирования по валидному запросу"""
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(valid_request),
                                content_type='application/json',
                                )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp['content-type'], 'application/json')

    def test_post_create_invalid_reservation(self):
        """Тест создания бронирования по невалидному запросу"""
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(invalid_request),
                                content_type='application/json',
                                )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp['content-type'], 'application/json')


class TestResponseIsValid(TestCase):

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

    def test_get_reservation_list_return_all_items(self):
        """Тест - валидность получения полного списка бронирований"""
        resp = self.client.get(reverse('reservation:reservation-list'))
        items = Reservation.objects.all()
        serializer = ReservationSerializer(items, many=True)
        self.assertEqual(resp.data, serializer.data)

    def test_get_reservation_today_list_return_all_items(self):
        """Тест - валидность получения полного списка бронирований на день вперед"""
        resp = self.client.get(reverse('reservation:reservation-today-list'))
        items = Reservation.objects.filter(
            room__reservation__start_meeting_time__gte=F('start_meeting_time')).filter(
            room__reservation__start_meeting_time__lte=F('start_meeting_time') + timedelta(days=1)).distinct()
        serializer = ReservationSerializer(items, many=True)
        self.assertEqual(resp.data, serializer.data)

    def test_get_reservation_room_today_list_return_item(self):
        """Тест - валидность получения списка бронирования переговорной {id} на день вперед """
        resp = self.client.get(reverse('reservation:reservation-room-today-list', args=[1, ]))

        item = Reservation.objects.filter(room=1)
        serializer = ReservationSerializer(item, many=True)
        self.assertEqual(resp.data, serializer.data)

    def test_get_reservation_detail_return_item(self):
        """Тест - валидность получения информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.get(reverse('reservation:reservation-detail', args=[id_num, ]))
            item = Reservation.objects.get(id=id_num)
            serializer = ReservationSerializer(item, many=False)
            self.assertEqual(resp.data, serializer.data)

    def test_put_reservation_detail_return_item(self):
        """Тест - валидность ответа изменения информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.put(reverse('reservation:reservation-detail', args=[id_num, ]),
                                   data=json.dumps(valid_request),
                                   content_type='application/json',
                                   )
            item = Reservation.objects.get(id=id_num)
            serializer = ReservationSerializer(item, many=False)
            self.assertEqual(resp.data, serializer.data)

    def test_patch_reservation_detail_return_item(self):
        """Тест - валидность ответа частичного изменения информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.patch(reverse('reservation:reservation-detail', args=[id_num, ]),
                                     data=json.dumps(valid_request),
                                     content_type='application/json',
                                     )
            item = Reservation.objects.get(id=id_num)
            serializer = ReservationSerializer(item, many=False)
            self.assertEqual(resp.data, serializer.data)

    def test_delete_reservation_detail_return_item(self):
        """Тест - валидность ответа удаления информации о бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.delete(reverse('reservation:reservation-detail', args=[id_num, ]))
            try:
                item = Reservation.objects.get(id=id_num)
                serializer = ReservationSerializer(item, many=False)
            except Reservation.DoesNotExist:
                self.assertTrue(True)
            else:
                self.assertEqual(resp.data, serializer.data)

    def test_post_create_valid_reservation_return_item(self):
        """Тест создания бронирования по валидному запросу"""
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(valid_request),
                                content_type='application/json',
                                )
        item = Reservation.objects.get(id=1)
        serializer = ReservationSerializer(item, many=False)
        self.assertEqual(resp.data, serializer.data)

    def test_post_create_invalid_reservation_return_item(self):
        """Тест создания бронирования по невалидному запросу"""
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(invalid_request),
                                content_type='application/json',
                                )
        try:
            item = Reservation.objects.get(id=1)
            serializer = ReservationSerializer(item, many=False)
        except Reservation.DoesNotExist:
            self.assertTrue(True)
        else:
            self.assertEqual(resp.data, serializer.data)
