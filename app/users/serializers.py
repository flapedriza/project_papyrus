from rest_framework import serializers

from .models import User


USER_FIELDS = ('email', 'first_name', 'last_name', 'created',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = USER_FIELDS + ('password',)
        extra_kwargs = {
            'created': {'read_only': True},
        }


class ProfileSerializer(UserSerializer):

    class Meta:
        model = User
        fields = USER_FIELDS
        partial = True
        extra_kwargs = {
            'email': {'read_only': True},
            'created': {'read_only': True},
        }