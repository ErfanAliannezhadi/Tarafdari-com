from rest_framework import serializers
from .models import UserModel, EmojiPackageModel
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = '__all__'
        read_only_fields = ['is_active', 'is_auther', 'is_admin', 'is_phone_verified', 'registration_date',
                            'last_online']


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmojiPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmojiPackageModel
        fields = '__all__'
        read_only_fields = ['from_user', 'to_user']
