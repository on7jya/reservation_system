from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny

from apps.users.api.serializers import PersonSerializer, UserLoginSerializer, UserRegisterSerializer
from apps.users.auth_model import UserAuth
from apps.users.models import Person


class ListPersonAPIView(generics.ListAPIView):
    """Список всех сотрудников"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class PersonAPIView(generics.RetrieveAPIView):
    """Информация по конкретному сотруднику {id}"""
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


@authentication_classes([])
@permission_classes([AllowAny])
class RegisterApi(generics.CreateAPIView):
    """Создание нового пользователя"""
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([AllowAny])
class UserLogin(generics.CreateAPIView):
    """Логин пользователя"""
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = UserAuth().do_login(request, request.data)
            data = UserLoginSerializer(user).data
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return JsonResponse('', status=status.HTTP_403_FORBIDDEN)
