import random
import datetime
from datetime import timedelta
from django.utils import timezone
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


def _random_string(length):
    """Возвращает идентификатор из 11 символов"""
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    chars_2 = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    return ''.join([random.choice(chars + chars_2) for i in range(0, length)])


def _random_date(start):
    """Возвращает рандомную дату между start и start+1 час"""
    delta = datetime.timedelta(hours=1)
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def _create_office_in_database(id_num):
    """Создадим офис"""
    office = Office.objects.create(id=id_num, name=_random_string(50))
    return office


def _create_user_in_database(id_num, office):
    """Создадим пользователя"""
    user = Person.objects.create(
        id=id_num,
        password=_random_string(11),
        username=_random_string(20),
        first_name=_random_string(10),
        last_name=_random_string(10),
        email=_random_string(10),
        office=office
    )
    return user


def _create_room_in_database(id_num, office):
    """Создадим переговорную"""
    room = Room.objects.create(
        id=id_num,
        name=_random_string(10),
        office=office,
        size=random.randint(1, 100),
        availability=True)
    return room


def _create_reservation_in_database(id_num, room, user, begin, end_date_correct):
    """Создадим бронирование"""
    if end_date_correct:
        reservation = Reservation.objects.create(
            id=id_num,
            room=room,
            created_by=user,
            subject=_random_string(50),
            start_meeting_time=_random_date(begin),
            end_meeting_time=_random_date(begin) + datetime.timedelta(hours=2))
    else:
        reservation = Reservation.objects.create(
            id=id_num,
            room=room,
            created_by=user,
            subject=_random_string(50),
            start_meeting_time=_random_date(begin),
            end_meeting_time=_random_date(begin) - datetime.timedelta(hours=2))
    return reservation


def random_data(id_num, end_date_correct):
    """Сгенерим полный набор данных"""
    office = _create_office_in_database(id_num)
    user = _create_user_in_database(id_num, office)
    room = _create_room_in_database(id_num, office)
    tz = timezone.get_current_timezone()
    begin = tz.localize(datetime.datetime(2116, 6, 1, 8, 0, 0))
    reservation = _create_reservation_in_database(id_num, room, user, begin, end_date_correct)
