import datetime
from datetime import timedelta

from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.reservation.managers import ReservationManager

PENDING = "0"
ACCEPTED = "1"
REJECTED = "2"
CHOICES_RESERVATION = [
    (PENDING, "В ожидании подтверждения"),
    (ACCEPTED, "Подтверждена"),
    (REJECTED, "Отменена")
]

MANUAL = "0"
AUTO = "1"
CHOICES_CANCELATION = [
    (MANUAL, "Ручная отмена"),
    (AUTO, "Автоматическая отмена"),
    (None, "Не отменена")
]


class Reservation(TimeStampedModel):
    room = models.ForeignKey('rooms.Room', null=False, blank=False,
                             on_delete=models.CASCADE,
                             verbose_name='Переговорная')
    created_by = models.ForeignKey('users.Person', null=False, blank=False,
                                   on_delete=models.CASCADE,
                                   verbose_name='Инициатор встречи')
    invited = models.ManyToManyField('users.Person', default=None, null=True, blank=True,
                                     related_name="invited",
                                     verbose_name='Участники встречи')
    subject = models.CharField(max_length=100, null=False, blank=False, verbose_name='Тема встречи')
    start_meeting_time = models.DateTimeField(null=False, blank=False, verbose_name='Время начала встречи')
    end_meeting_time = models.DateTimeField(null=False, blank=False, verbose_name='Время окончания встречи')
    cancel_reservation_time = models.DateTimeField(null=True, blank=True, verbose_name='Время отмены бронирования')
    state = models.CharField(max_length=1, null=True, blank=True, default="0", choices=CHOICES_RESERVATION,
                             verbose_name='Состояние бронирования')
    state_canceled = models.CharField(max_length=1, null=True, blank=True, default=None, choices=CHOICES_CANCELATION,
                                      verbose_name='Состояние отмены брони')

    objects = ReservationManager()

    def auto_cancel(self):
        if self.state == "0":
            self.state = "2"
            self.state_canceled = "1"
            self.cancel_reservation_time = self.start_meeting_time + timedelta(minutes=15)

    def manual_cancel(self):
        if self.state == "0":
            self.state = "2"
            self.state_canceled = "0"
            self.cancel_reservation_time = datetime.datetime.now()

    def accept(self):
        if self.state == "0":
            self.state = "1"

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["start_meeting_time"]

    def __str__(self):
        return self.subject
