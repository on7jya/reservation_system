from datetime import datetime, timedelta, time

from pytz.reference import LocalTimezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.reservation.models import Reservation
from config.settings import START_WORK_OFFICE, END_WORK_OFFICE


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
            raise ValidationError({'end_meeting_time': 'Meeting cannot last more than 1 day'})
        if attrs['start_meeting_time'].time() < START_WORK_OFFICE:
            raise ValidationError({'start_meeting_time': 'Start date should be upper {}'.format(START_WORK_OFFICE)})
        if attrs['end_meeting_time'].time() > END_WORK_OFFICE:
            raise ValidationError({'end_meeting_time': 'End date should be lower {}'.format(END_WORK_OFFICE)})
        return attrs


class ReservationIdSerializer(serializers.Serializer):
    reservation = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Reservation.objects.all().only('id'),
        required=True
    )
