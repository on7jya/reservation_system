from rest_framework import generics

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.models import Person
from .serializers import PersonSerializer, RegistrationSerializer


# @permission_classes([IsAuthenticated])
class ListPersonAPIView(generics.ListAPIView):
    """Список всех сотрудников"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonAPIView(generics.RetrieveAPIView):
    """Иныормация по конкретному сотруднику {id}"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

#
# @api_view(['POST',])
# def registration_view(request):
#     """Регистрация нового сотрудника (требуется username, password и password2 в post)"""
#     serializer = RegistrationSerializer(data=request.data)
#     data = {}
#     if serializer.is_valid():
#         account = serializer.save()
#         data['response'] = "Successfully register a new user."
#         data['email'] = account.email
#         data['username'] = account.username
#         token = Token.objects.get(user=account).key
#         data['token'] = token
#     else:
#         data = serializer.errors
#     return Response(data)


@authentication_classes([])
@permission_classes([AllowAny])
class RegisterApi(generics.CreateAPIView):
    # http_method_names = ['POST']
    # permission_classes = []
    model = Person
    serializer_class = RegistrationSerializer
    # queryset = Person.objects.all()

