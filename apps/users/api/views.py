from rest_framework import generics

from apps.users.models import Person
from apps.users.api.serializers import PersonSerializer


class ListPersonAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

