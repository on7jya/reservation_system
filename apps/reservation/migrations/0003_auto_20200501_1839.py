# Generated by Django 2.2.2 on 2020-05-01 15:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_auto_20200501_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='cancel_reservation_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время отмены бронирования'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='invited',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='invited', to=settings.AUTH_USER_MODEL, verbose_name='Участники встречи'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='state',
            field=models.CharField(blank=True, choices=[('0', 'В ожидании подтверждения'), ('1', 'Подтверждена'), ('2', 'Отменена')], default='0', max_length=1, null=True, verbose_name='Состояние бронирования'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='state_canceled',
            field=models.CharField(blank=True, choices=[('0', 'Ручная отмена'), ('1', 'Автоматическая отмена'), (None, 'Не отменена')], default=None, max_length=1, null=True, verbose_name='Состояние отмены брони'),
        ),
    ]
