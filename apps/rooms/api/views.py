from rest_framework import generics
from rest_framework.generics import get_object_or_404

from apps.rooms.models import Office, Room, Equipment
from apps.rooms.api.serializers import OfficeSerializer, RoomsSerializer, EquipmentSerializer
from apps.users.models import Person
from apps.users.api.serializers import PersonSerializer


# GET list
class ListOfficeAPIView(generics.ListAPIView):
    """Список всех офисов"""
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()


class ListRoomAPIView(generics.ListAPIView):
    """Список всех переговорных"""
    serializer_class = RoomsSerializer
    queryset = Room.objects.all()


class ListEquipmentAPIView(generics.ListAPIView):
    """Список всего оборудования"""
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()


class ListRoomsInOfficeAPIView(generics.ListAPIView):
    """Список всех переговорных в офисе"""
    serializer_class = RoomsSerializer

    def get_queryset(self):
        office = self.kwargs.get('pk')
        return Room.objects.filter(office__room=office)


class ListPersonsInOfficeAPIView(generics.ListAPIView):
    """Список всех сотрудников в офисе {id}"""
    serializer_class = PersonSerializer

    def get_queryset(self):
        office = self.kwargs.get('pk')
        return Person.objects.filter(office__room=office)


class ListEquipmentsInRoomAPIView(generics.ListAPIView):
    """Список всего оборудования в переговорной {id}"""
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        room = self.kwargs.get('pk')
        return Equipment.objects.filter(room__equipment=room)


##########################################

# GET + POST
class OfficeAPIView(generics.RetrieveAPIView):
    """Информация по конкретному офису {id}"""
    serializer_class = OfficeSerializer
    queryset = Office.objects.all()


class RoomAPIView(generics.RetrieveAPIView):
    """Информация по конкретной переговорной {id}"""
    serializer_class = RoomsSerializer
    queryset = Room.objects.all()


class EquipmentAPIView(generics.RetrieveAPIView):
    """Информация по конкретной единице оборудования {id}"""
    serializer_class = EquipmentSerializer
    queryset = Equipment.objects.all()
