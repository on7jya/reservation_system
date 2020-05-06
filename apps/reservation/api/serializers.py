from rest_framework import serializers

from apps.reservation.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "created", "created_by", "modified", "room", "subject",
                  "start_meeting_time", "end_meeting_time", "cancel_reservation_time",
                  "state", "state_canceled"]
