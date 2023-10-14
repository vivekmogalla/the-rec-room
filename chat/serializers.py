from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Chat, ChatMessage


class ChatSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('id', 'users', 'modified_at_formatted', 'archived',)


class ChatMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%b %d, %Y %I:%M%p')

    class Meta:
        model = ChatMessage
        fields = ('id', 'sent_to', 'created_by', 'created_at', 'body', 'viewed',)


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Chat
        fields = ('id', 'users', 'modified_at_formatted', 'messages',)