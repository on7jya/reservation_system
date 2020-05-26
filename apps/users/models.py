from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from rest_framework.authtoken.models import Token

from apps.reservation.signals import post_save_handler, post_delete_handler


class Person(AbstractUser):
    office = models.ForeignKey('rooms.Office', on_delete=models.SET_NULL, default=None, null=True, verbose_name='Офис')

    class Meta:
        db_table = 'users'
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_login"]

    def __str__(self):
        if not self.last_name or not self.first_name:
            return f"{self.username}"
        else:
            return f"{self.last_name} {self.first_name}"

    @property
    def auth_token(self):
        return Token.objects.get(user=self.pk).key


post_save.connect(post_save_handler, sender=Person)
post_delete.connect(post_delete_handler, sender=Person)
