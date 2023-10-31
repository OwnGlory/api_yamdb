import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ]
    )

    def validate_username(self, value):
        if not re.match('^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать патерну ^[\w.@+-]+\Z')
        return value

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = MyUser


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = MyUser
        read_only_fields = ('role',)
    
    def validate_username(self, value):
        if not re.match('^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать патерну ^[\w.@+-]+\Z')
        return value

class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,

    )
    email = serializers.EmailField(
        max_length=254,

    )

    

    def validate_username(self, value):
        if not re.match('^[\w.@+-]+\Z', value):
            raise serializers.ValidationError('usermane должен соответсвовать патерну ^[\w.@+-]+\Z')

        if value == 'me':
            raise serializers.ValidationError('Username "me" is not valid')
        return value

    class Meta:
        fields = ('username', 'email')
        model = MyUser


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
