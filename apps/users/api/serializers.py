from rest_framework import serializers

from apps.users.models import Person
from apps.rooms.models import Office


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'office']


class RegistrationSerializer(serializers.ModelSerializer):

    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    auth_token = serializers.CharField(max_length=64, required=False)

    class Meta:
        model = Person
        fields = ['username', 'email', 'password', 'auth_token']  # , 'password2'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    # def save(self):
    #     user = Person(
    #             username=self.validated_data['username'],
    #     )
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']
    #
    #     if password != password2:
    #         raise serializers.ValidationError({'password': 'Passwords must match.'})
    #     user.set_password(password)
    #     user.save()
    #     return user
