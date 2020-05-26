from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.auth_model import UserAuth
from apps.users.models import Person


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор объекта пользователя"""

    class Meta:
        model = Person
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'office']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор объекта пользователя для регистрации"""
    token = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'token',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_token(self, obj):
        return Token.objects.get(user=obj).key

    def create(self, validated_data):
        return UserAuth().prepare_new_user(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """Сериализатор объекта пользователя для логина"""
    token = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'token',)
        extra_kwargs = {
            'email': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'password': {'write_only': True},
        }

    def get_token(self, obj):
        return Token.objects.get(user=obj).key
