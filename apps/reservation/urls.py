from django.urls import path

from apps.reservation.api.views import (
    ListReservationAPIView,
    ReservationAPIView
)

app_name = "reservation"

urlpatterns = [
    path("list/", ListReservationAPIView.as_view(), name='reservation'),
    path("<slug:pk>/", ReservationAPIView.as_view(), name='reservation-detail'),
]
