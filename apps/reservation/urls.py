from django.conf.urls import url, include
from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.reservation.api.views import (
    ListReservationAPIView,
    ReservationAPIView,
    AddReservationAPIView,
    ListReservationTodayAPIView,
    ListReservationRoomTodayAPIView,
    ApproveReservationView,
    CancelReservationView
)

app_name = "reservation"

router = DefaultRouter(trailing_slash=False)
router.register(r'', ListReservationAPIView)

urlpatterns = [
    url(r"list/", include(router.urls), name='reservation-list'),
    path("list/today/", ListReservationTodayAPIView.as_view(), name='reservation-today-list'),
    path("list/today/<slug:pk>", ListReservationRoomTodayAPIView.as_view(), name='reservation-room-today-list'),
    path("<slug:pk>", ReservationAPIView.as_view(), name='reservation-detail'),
    path("<slug:pk>/approve/", ApproveReservationView.as_view(), name='reservation-approve'),
    path("<slug:pk>/reject/", CancelReservationView.as_view(), name='reservation-reject'),
    path("add/", AddReservationAPIView.as_view(), name='reservation-create'),
]
