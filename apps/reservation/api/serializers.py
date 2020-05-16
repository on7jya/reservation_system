from datetime import datetime

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
        return attrs


class ReservationIdSerializer(serializers.Serializer):
    reservation = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Reservation.objects.all().only('id'),
        required=True
    )
