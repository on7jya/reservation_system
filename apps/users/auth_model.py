from datetime import datetime

import pytz
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.models import Person


class UserAuth:

    def email_is_used(self, email: str) -> bool:
        """Проверка на существование email"""
        if email is not None:
            return Person.objects.filter(email=email).exists()
        return False

    def create_new_user(self, data: object) -> Person:
        """Создать нового юзера"""
        new_user = Person.objects.create_user(data.get('username'), data.get('email'), data.get('password'))
        new_user.first_name = data.get('first_name')
        new_user.last_name = data.get('last_name')
        new_user.last_login = datetime.now(tz=pytz.utc)
        new_user.save()
        return new_user

    def get_token(self, user):
        """Получить/создать токен"""
        return Token.objects.get_or_create(user=user)

    def prepare_new_user(self, data):
        """Подготовка нового юзера"""
        email = data.get('email', None)
        if not self.email_is_used(email):
            new_user = self.create_new_user(data)
            user = authenticate(username=data.get('username'), password=data.get('password'))
            self.get_token(user)
            return new_user
        raise serializers.ValidationError({'email_used': 'This email is already used.'})

    def do_login(self, request, data):
        """Логин"""
        try:
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None and user.is_active:
                login(request, user)
                self.get_token(user)
                return user
        except Person.DoesNotExist:
            raise serializers.ValidationError({'login_error': 'Email or password wrong.'})
