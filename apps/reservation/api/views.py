from rest_framework import generics

from apps.reservation.models import Reservation
from apps.reservation.api.serializers import ReservationSerializer


class ListReservationAPIView(generics.ListCreateAPIView):
    """Список всех бронирований"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ReservationAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Информация о конкретном бронировании {id}"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
