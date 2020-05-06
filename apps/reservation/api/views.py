from django.db.models import F
from rest_framework import generics
from datetime import timedelta
from apps.reservation.models import Reservation
from apps.reservation.api.serializers import ReservationSerializer


class ListReservationAPIView(generics.ListAPIView):
    """Список всех бронирований"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class AddReservationAPIView(generics.CreateAPIView):
    """Добавить новое бронирование"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ReservationAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Информация о конкретном бронировании {id}"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class ListReservationTodayAPIView(generics.ListAPIView):
    """Список всех бронирований на день вперед"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.filter(
        room__reservation__start_meeting_time__gte=F('start_meeting_time')).filter(
        room__reservation__start_meeting_time__lte=F('start_meeting_time') + timedelta(days=1)).distinct()


class ListReservationRoomTodayAPIView(generics.ListAPIView):
    """Список бронирований переговорной {id} на день вперед"""
    serializer_class = ReservationSerializer

    def get_queryset(self):
        room = self.kwargs.get('pk')
        return Reservation.objects.filter(
            room__reservation__start_meeting_time__gte=F('start_meeting_time')).filter(
            room__reservation__start_meeting_time__lte=F('start_meeting_time') + timedelta(days=1)).filter(
            room_id=room).distinct()
