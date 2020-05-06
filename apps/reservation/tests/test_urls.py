import json
from django.test import TestCase
from django.urls import reverse
from apps.rooms.models import Room, Office
from apps.users.models import Person

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
        office = Office.objects.create(id=1, name='Департамент Х5')
        user = Person.objects.create(
            id=1, password='testtest', username='test_enroll',
            first_name='Тестер', last_name='Батькович',
            email='test_enroll@test.ru', office=office
        )
        room = Room.objects.create(id=1, name='Ока', office=office, size='15', availability=True)

    def test_reservation_list(self):
        resp = self.client.get(reverse('reservation:reservation-list'))
        self.assertEqual(resp.status_code, 200)

    def test_reservation_today_list(self):
        resp = self.client.get(reverse('reservation:reservation-today-list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_valid_reservation(self):
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(valid_request),
                                content_type='application/json',
                                )
        self.assertEqual(resp.status_code, 201)

    def test_create_invalid_reservation(self):
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(invalid_request),
                                content_type='application/json',
                                )
        self.assertEqual(resp.status_code, 400)

    def test_reservation_room_today_list(self):
        resp = self.client.get(reverse('reservation:reservation-room-today-list', args=[1,]))
        self.assertEqual(resp.status_code, 200)

