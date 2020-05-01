from django.urls import path

from apps.reservation.api.views import (
    ListReservationAPIView,
    ReservationAPIView,
    AddReservationAPIView
)

app_name = "reservation"

urlpatterns = [
    path("list/", ListReservationAPIView.as_view(), name='reservation-list'),
    path("<slug:pk>", ReservationAPIView.as_view(), name='reservation-detail'),
    path("add/", AddReservationAPIView.as_view(), name='reservation-create'),
]
