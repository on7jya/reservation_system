from datetime import datetime, timedelta, time

from pytz.reference import LocalTimezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "created", "created_by", "modified", "room", "subject",
                  "start_meeting_time", "end_meeting_time", "cancel_reservation_time",
                  "state", "state_canceled"]

    def validate(self, attrs):
        if attrs['start_meeting_time'] >= attrs['end_meeting_time']:
            raise ValidationError({'end_meeting_time': 'End date should be after start date'})
        if attrs['start_meeting_time'] <= datetime.now(LocalTimezone()):
            raise ValidationError({'start_meeting_time': 'Start date should be after current date'})
        if attrs['end_meeting_time'] - attrs['start_meeting_time'] >= timedelta(days=1):
            raise ValidationError({'start_meeting_time': 'Meeting cannot last more than 1 day'})
        if attrs['start_meeting_time'].time() < time(hour=8, minute=0, second=0):
            raise ValidationError({'end_meeting_time': 'Start date should be upper 08.00'})
        if attrs['end_meeting_time'].time() > time(hour=22, minute=0, second=0):
            raise ValidationError({'end_meeting_time': 'End date should be lower 22.00'})
        return attrs


class ReservationIdSerializer(serializers.Serializer):
    reservation = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Reservation.objects.all().only('id'),
        required=True
    )
