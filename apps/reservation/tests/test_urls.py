import json
from django.test import TestCase
from django.urls import reverse
from apps.rooms.models import Room, Office
from apps.users.models import Person
from apps.reservation.models import Reservation

valid_request = {
    "created_by": "1",
    "room": "1",
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


class TestUrlsHttpResponse(TestCase):

    def setUp(self):
        """Тестовые данные"""
        office = Office.objects.create(id=1, name='Департамент Х5')
        user = Person.objects.create(
            id=1, password='testtest', username='test_enroll',
            first_name='Тестер', last_name='Батькович',
            email='test_enroll@test.ru', office=office
        )
        room = Room.objects.create(id=1, name='Ока', office=office, size='15', availability=True)
        reservation = Reservation.objects.create(id=9999, room=room, created_by=user, subject='Бронь',
                                                 start_meeting_time='2020-05-06T16:42:20.880Z',
                                                 end_meeting_time='2020-05-06T18:42:20.880Z')

    def test_get_reservation_list(self):
        """Тест получения полного списка бронирований"""
        resp = self.client.get(reverse('reservation:reservation-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_reservation_today_list(self):
        """Тест получения полного списка бронирований на день вперед"""
        resp = self.client.get(reverse('reservation:reservation-today-list'))
        self.assertEqual(resp.status_code, 200)

    def test_get_reservation_room_today_list(self):
        """Тест получения списка бронирования переговорной {id} на день вперед """
        resp = self.client.get(reverse('reservation:reservation-room-today-list', args=[1, ]))
        self.assertEqual(resp.status_code, 200)

    def test_get_reservation_detail(self):
        """Тест получения информации о бронирования {id} """
        resp = self.client.get(reverse('reservation:reservation-detail', args=[9999, ]))
        self.assertEqual(resp.status_code, 200)

    def test_put_reservation_detail(self):
        """Тест изменения информации о бронирования {id} """
        resp = self.client.put(reverse('reservation:reservation-detail', args=[9999, ]),
                               data=json.dumps(valid_request),
                               content_type='application/json',
                               )
        self.assertEqual(resp.status_code, 200)

    def test_patch_reservation_detail(self):
        """Тест частичного изменения информации о бронирования {id} """
        resp = self.client.patch(reverse('reservation:reservation-detail', args=[9999, ]),
                                 data=json.dumps(valid_request),
                                 content_type='application/json',
                                 )
        self.assertEqual(resp.status_code, 200)

    def test_delete_reservation_detail(self):
        """Тест удаления информации о бронирования {id} """
        resp = self.client.delete(reverse('reservation:reservation-detail', args=[9999, ]))
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

    def test_post_create_invalid_reservation(self):
        """Тест создания бронирования по невалидному запросу"""
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(invalid_request),
                                content_type='application/json',
                                )
        self.assertEqual(resp.status_code, 400)
