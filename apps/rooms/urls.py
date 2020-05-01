from django.urls import path

from apps.rooms.api.views import (
    ListOfficeAPIView,
    ListRoomAPIView,
    ListEquipmentAPIView,
    OfficeAPIView,
    RoomAPIView,
    EquipmentAPIView
)

app_name = "rooms"

urlpatterns = [
    path("office/list/", ListOfficeAPIView.as_view(), name='office'),
    path("office/<slug:pk>/", OfficeAPIView.as_view(), name='office-detail'),

    path("room/list/", ListRoomAPIView.as_view(), name='room'),
    path("room/<slug:pk>/", RoomAPIView.as_view(), name='room-detail'),

    path("equipment/list/", ListEquipmentAPIView.as_view(), name='equipment'),
    path("equipment/<slug:pk>/", EquipmentAPIView.as_view(), name='equipment-detail'),
]
