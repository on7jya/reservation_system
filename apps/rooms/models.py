from django.db import models


class Office(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование офиса')

    class Meta:
        verbose_name = "Офис"
        verbose_name_plural = "Офисы"
        ordering = ["name"]

    def __str__(self):
        return self.name



class Rooms(models.Model):
    name = models.CharField(max_length=100)
    office = models.ForeignKey('reservation.Office', on_delete=models.CASCADE)
    size = models.IntegerField
    availability = models.BooleanField

    class Meta:
        verbose_name = "Переговорная"
        verbose_name_plural = "Переговорные"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Equipment(models.Model):
    eq_type = models.CharField(max_length=80)
    office = models.ForeignKey('reservation.Office', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["eq_type"]

    def __str__(self):
        return self.eq_type

