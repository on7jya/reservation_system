from django.urls import path

from apps.reservation.api.views import (
    ListReservationAPIView,
    ReservationAPIView,
    AddReservationAPIView,
    ListReservationTodayAPIView,
    ListReservationRoomTodayAPIView
)

app_name = "reservation"

urlpatterns = [
    path("list/", ListReservationAPIView.as_view(), name='reservation-list'),
    path("list/today/", ListReservationTodayAPIView.as_view(), name='reservation-today-list'),
    path("list/today/<slug:pk>", ListReservationRoomTodayAPIView.as_view(), name='reservation-room-today-list'),
    path("<slug:pk>", ReservationAPIView.as_view(), name='reservation-detail'),
    path("add/", AddReservationAPIView.as_view(), name='reservation-create'),
]
