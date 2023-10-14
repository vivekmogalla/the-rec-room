from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'get_avatar',)


class UserFollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer(read_only=True, many=True)
    followed_by = UserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'get_avatar', 'follows', 'followed_by',)