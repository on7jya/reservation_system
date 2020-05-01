from rest_framework import generics

from apps.users.models import Person
from apps.users.api.serializers import PersonSerializer


class ListPersonAPIView(generics.ListAPIView):
    """Список всех сотрудников"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonAPIView(generics.RetrieveAPIView):
    """Иныормация по конкретному сотруднику {id}"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
