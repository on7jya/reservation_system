from rest_framework import generics

from apps.reservation.models import Reservation
from apps.reservation.api.serializers import ReservationSerializer


class ListReservationAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ReservationAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
