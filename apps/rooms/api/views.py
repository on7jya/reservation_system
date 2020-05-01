from rest_framework import generics

from apps.rooms.models import Office, Room, Equipment
from apps.rooms.api.serializers import OfficeSerializer, RoomsSerializer, EquipmentSerializer


# GET list
class ListOfficeAPIView(generics.ListAPIView):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()


class ListRoomAPIView(generics.ListAPIView):
    serializer_class = RoomsSerializer
    queryset = Room.objects.all()


class ListEquipmentAPIView(generics.ListAPIView):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()


##########################################

# POST PUT PATCH DELETE
class OfficeAPIView(generics.RetrieveAPIView):
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()


class RoomAPIView(generics.RetrieveAPIView):
    serializer_class = RoomsSerializer
    queryset = Room.objects.all()


class EquipmentAPIView(generics.RetrieveAPIView):
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
