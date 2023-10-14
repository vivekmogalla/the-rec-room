from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def notifications(request):
  new_notifications = request.user.received_notifications.filter(is_read=False).order_by('-created_at')
  newSerializer = NotificationSerializer(new_notifications, many=True)

  read_notifications = request.user.received_notifications.filter(is_read=True).order_by('-created_at')[:16]
  readSerializer = NotificationSerializer(read_notifications, many=True)

  return JsonResponse({
    'newNotifications': newSerializer.data,
    'readNotifications': readSerializer.data,
  }, safe=False)

@api_view(['POST'])
def read_notification(request, id):
  status = request.data.get('status')
  message = 'notification read'
  notification = Notification.objects.get(pk=id)
  
  if status == 'is_read':
    notification.is_read = False
    message = 'notification unread'
  else:
    notification.is_read = True
  
  notification.save()

  return JsonResponse({'message': message})

@api_view(['POST'])
def read_all_notifications(request):
  new_notifications = request.user.received_notifications.filter(is_read=False)

  for notification in new_notifications:
    notification.is_read = True
    notification.save()

  return JsonResponse({'message': 'mark all notifications read'})