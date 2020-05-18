from rest_framework import generics

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from apps.users.models import Person
from .serializers import PersonSerializer, RegistrationSerializer


class ListPersonAPIView(generics.ListAPIView):
    """Список всех сотрудников"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonAPIView(generics.RetrieveAPIView):
    """Иныормация по конкретному сотруднику {id}"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

@api_view(['POST',])
def registration_view(request):

    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = "Successfully register a new user."
        data['email'] = account.email
        data['username'] = account.username
        token = Token.objects.get(user=account).key
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)
