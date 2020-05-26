from rest_framework import serializers

from apps.rooms.models import Office, Room, Equipment


class OfficeSerializer(serializers.ModelSerializer):
    """Сериализатор объекта офиса"""
    class Meta:
        model = Office
        fields = ('id', 'name')


class RoomsSerializer(serializers.ModelSerializer):
    """Сериализатор объекта переговорной комнаты"""
    office = OfficeSerializer

    class Meta:
        model = Room
        fields = ['id', 'name', 'office', 'size', 'availability']


class EquipmentSerializer(serializers.ModelSerializer):
    """Сериализатор объекта оборудования"""
    office = OfficeSerializer

    class Meta:
        model = Equipment
        fields = ['id', 'eq_type', 'room']
