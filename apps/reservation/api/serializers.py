from rest_framework import serializers

from apps.reservation.models import Office, Person


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('id', 'name')


class PersonSerializer(serializers.ModelSerializer):
    office = OfficeSerializer

    class Meta:
        model = Person
        fields = ['id', 'last_name', 'first_name', 'email', 'office']
