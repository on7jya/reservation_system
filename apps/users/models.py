from django.db import models
from django.contrib.auth.models import AbstractUser

from config import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Person(AbstractUser):
    office = models.ForeignKey('rooms.Office', on_delete=models.SET_NULL, default=None, null=True, verbose_name='Офис')




    class Meta:
        db_table = 'users'
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_login"]



    def __str__(self):
        return f"{self.last_name} {self.first_name}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
