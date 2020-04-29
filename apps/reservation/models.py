from django.db import models
from django.contrib.auth.models import AbstractUser


class Office(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование офиса')

    class Meta:
        verbose_name = "Офис"
        verbose_name_plural = "Офисы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Person(AbstractUser):
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, default=None, null=True, verbose_name='Офис')

    class Meta:
        db_table = 'users'
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_login"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
