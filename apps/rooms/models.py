from django.db import models


class Office(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование офиса')

    class Meta:
        verbose_name = "Офис"
        verbose_name_plural = "Офисы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование переговорной')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='Офис')
    size = models.IntegerField(verbose_name='Вместимость')
    availability = models.BooleanField(verbose_name='Доступность для бронирования')

    class Meta:
        verbose_name = "Переговорная"
        verbose_name_plural = "Переговорные"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Equipment(models.Model):
    eq_type = models.CharField(max_length=80, verbose_name='Тип оборудования')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Переговорная')

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["eq_type"]

    def __str__(self):
        return self.eq_type
