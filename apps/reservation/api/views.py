from datetime import timedelta

from django.db.models import F
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, filters, viewsets

from apps.reservation.api import docs
from apps.reservation.api.serializers import ReservationSerializer, ReservationIdSerializer
from apps.reservation.models import Reservation
from apps.reservation.services import ApproveReservationService, CancelReservationService


class DateRangeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'start_date_range' in request.GET and 'end_date_range' in request.GET:
            if request.GET['end_date_range'] < request.GET['start_date_range']:
                return []
            else:
                return queryset.filter(
                    start_meeting_time__lte=request.GET['end_date_range'],
                    end_meeting_time__gte=request.GET['start_date_range']
                )
        return queryset


class ListReservationAPIView(viewsets.ReadOnlyModelViewSet):
    """Список всех бронирований/Список всех бронирований переговорной {id}"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    filter_backends = (DateRangeFilter,)


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


@method_decorator(name='get', decorator=swagger_auto_schema(**docs.reservation_approve))
class ApproveReservationView(generics.GenericAPIView):
    """Подтверждение бронирования {id}"""
    serializer_class = ReservationIdSerializer
    queryset = Reservation.objects.all()

    def get(self, request, *args, **kwargs):
        self.perform_action(request)

    def perform_action(self, request):
        ApproveReservationService(request=request, reservation=self.get_object()).execute()


@method_decorator(name='get', decorator=swagger_auto_schema(**docs.reservation_cancel))
class CancelReservationView(generics.GenericAPIView):
    """Ручная отмена бронирования {id}"""
    serializer_class = ReservationIdSerializer
    queryset = Reservation.objects.all()

    def get(self, request, *args, **kwargs):
        self.perform_action(request)

    def perform_action(self, request):
        CancelReservationService(request=request, reservation=self.get_object()).execute()
