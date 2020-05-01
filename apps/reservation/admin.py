from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "start_meeting_time", "end_meeting_time",
                    "cancel_reservation_time", "state", "state_canceled", "created_by_id",
                    "room_id"]
    search_fields = ["id", "subject"]
