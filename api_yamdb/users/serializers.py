import re
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=(
            UniqueValidator(queryset=MyUser.objects.all()),
        )
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(
            UniqueValidator(queryset=MyUser.objects.all()),
        )
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = MyUser

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать'
                                              'патерну ^[\\w.@+-]+\\Z')
        return value


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = MyUser
        read_only_fields = ('role',)

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать'
                                              'патерну ^[\\w.@+-]+\\Z')
        return value


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,

    )
    email = serializers.EmailField(
        max_length=254,

    )

    class Meta:
        fields = ('username', 'email')
        model = MyUser

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать'
                                              'патерну ^[\\w.@+-]+\\Z')

        if value == 'me':
            raise serializers.ValidationError('Username "me" is not valid')
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        get_object_or_404(MyUser, username=value)
        return value

    @classmethod
    def get_token(cls, user):
        get_object_or_404(MyUser, username=user)
        token = super().get_token(user)
        token['name'] = user.name
        return token


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
