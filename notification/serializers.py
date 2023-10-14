from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
  created_at = serializers.DateTimeField(format='%b %d, %Y %I:%M%p')
  created_by = UserSerializer(read_only=True)

  class Meta:
    model = Notification
    fields = ('id', 'body', 'type_of_notification', 'post_id', 'created_for_id', 'created_at', 'created_by', 'is_read',)