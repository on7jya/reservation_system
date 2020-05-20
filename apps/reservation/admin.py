from django.contrib import admin

from apps.reservation.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "room", "start_meeting_time", "end_meeting_time",
                    "cancel_reservation_time", "state", "state_canceled", "created_by"]
    search_fields = ["id", "subject"]
