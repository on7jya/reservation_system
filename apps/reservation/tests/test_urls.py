import json
from datetime import timedelta

from django.db.models import F
from django.test import TestCase
from django.urls import reverse

from apps.reservation.api.serializers import ReservationSerializer
from apps.reservation.models import Reservation
from apps.reservation.tests.base import valid_request, invalid_request, random_data


class TestUrlsHttpResponse(TestCase):
    """Тестирование отдаваемых сервером HTTP ответов при наличии данных"""

    def setUp(self):
        """Тестовые данные"""
        for id_num in range(10, 100, 1):
            random_data(id_num, True)

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

    def test_put_valid_reservation_detail(self):
        """Тест изменения информации о бронирования {id} - валидный запрос"""
        for id_num in range(10, 100, 1):
            resp = self.client.put(reverse('reservation:reservation-detail', args=[id_num, ]),
                                   data=json.dumps(valid_request),
                                   content_type='application/json',
                                   )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_put_invalid_reservation_detail(self):
        """Тест изменения информации о бронирования {id} - невалидный запрос"""
        for id_num in range(10, 100, 1):
            original_reservation = Reservation.objects.get(pk=id_num)
            resp = self.client.put(reverse('reservation:reservation-detail', args=[id_num, ]),
                                   data=json.dumps(invalid_request),
                                   content_type='application/json',
                                   )
            new_reservation = Reservation.objects.get(pk=id_num)
            self.assertEqual(original_reservation, new_reservation)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_patch_valid_reservation_detail(self):
        """Тест частичного изменения информации о бронирования {id} - валидный запрос """
        for id_num in range(10, 100, 1):
            resp = self.client.patch(reverse('reservation:reservation-detail', args=[id_num, ]),
                                     data=json.dumps(valid_request),
                                     content_type='application/json',
                                     )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_patch_invalid_reservation_detail(self):
        """Тест частичного изменения информации о бронирования {id} - невалидный запрос"""
        for id_num in range(10, 100, 1):
            original_reservation = Reservation.objects.get(pk=id_num)
            resp = self.client.patch(reverse('reservation:reservation-detail', args=[id_num, ]),
                                     data=json.dumps(invalid_request),
                                     content_type='application/json',
                                     )
            new_reservation = Reservation.objects.get(pk=id_num)
            self.assertEqual(original_reservation, new_reservation)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(resp['content-type'], 'application/json')

    def test_delete_valid_reservation_detail(self):
        """Тест удаления существующего бронирования {id} """
        for id_num in range(10, 100, 1):
            resp = self.client.delete(reverse('reservation:reservation-detail', args=[id_num, ]))
            self.assertEqual(resp.status_code, 204)
            # A successful response SHOULD be 200 (OK) if the response includes an entity describing the status,
            # 202 (Accepted) if the action has not yet been enacted,
            # or 204 (No Content) if the action has been enacted but the response does not include an entity.

    def test_delete_invalid_reservation_detail(self):
        """Тест удаления несуществующего бронирования {id} """
        for id_num in range(100, 1000, 100):
            resp = self.client.delete(reverse('reservation:reservation-detail', args=[id_num, ]))
            self.assertEqual(resp.status_code, 404)

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
        count_before = Reservation.objects.count()
        resp = self.client.post(reverse('reservation:reservation-create'),
                                data=json.dumps(invalid_request),
                                content_type='application/json',
                                )
        count_after = Reservation.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp['content-type'], 'application/json')


class TestResponseIsValid(TestCase):

    def setUp(self):
        """Тестовые данные"""
        for id_num in range(10, 100, 1):
            random_data(id_num, True)

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
