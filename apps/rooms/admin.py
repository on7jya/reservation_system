from django.contrib import admin

from apps.rooms.models import Office, Room, Equipment


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "office", "size", "availability"]
    search_fields = ["id", "name"]


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "eq_type"]
    search_fields = ["id"]
