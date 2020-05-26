from django.urls import path

from apps.rooms.api.views import (
    ListOfficeAPIView,
    ListRoomAPIView,
    ListEquipmentAPIView,
    OfficeAPIView,
    RoomAPIView,
    EquipmentAPIView,
    ListRoomsInOfficeAPIView,
    ListPersonsInOfficeAPIView,
    ListEquipmentsInRoomAPIView
)

app_name = "rooms"

urlpatterns = [
    path("office/list/", ListOfficeAPIView.as_view(), name='office-list'),
    path("office/<slug:pk>/", OfficeAPIView.as_view(), name='office-detail'),
    path("office/<slug:pk>/rooms/", ListRoomsInOfficeAPIView.as_view(), name='room-in-office-list'),
    path("office/<slug:pk>/users/", ListPersonsInOfficeAPIView.as_view(), name='users-in-office-list'),

    path("room/list/", ListRoomAPIView.as_view(), name='room-list'),
    path("room/<slug:pk>/", RoomAPIView.as_view(), name='room-detail'),
    path("room/<slug:pk>/equipment/", ListEquipmentsInRoomAPIView.as_view(), name='equipment-in-room-list'),

    path("equipment/list/", ListEquipmentAPIView.as_view(), name='equipment-list'),
    path("equipment/<slug:pk>/", EquipmentAPIView.as_view(), name='equipment-detail'),
]
