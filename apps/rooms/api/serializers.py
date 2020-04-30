from rest_framework import serializers

from apps.rooms.models import Office, Rooms, Equipment


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('id', 'name')


class RoomsSerializer(serializers.ModelSerializer):
    office = OfficeSerializer

    class Meta:
        model = Rooms
        fields = ['id', 'name', 'office', 'size', 'availability']

class EquipmentSerializer(serializers.ModelSerializer):
    office = OfficeSerializer

    class Meta:
        model = Rooms
        fields = ['id', 'eq_type', 'office']
