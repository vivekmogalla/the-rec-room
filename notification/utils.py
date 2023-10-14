from .models import Notification

from post.models import Post
from account.models import User

def create_notification(request, type_of_notification, post_id=None, recipient_id=None):
  created_for = None
  created_by = request.user

  if type_of_notification == 'post_like':
    body = f'{request.user.name} @{request.user.username} liked your rec!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'post_save':
    body = f'{request.user.name} @{request.user.username} saved your rec!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'post_comment':
    body = f'{request.user.name} @{request.user.username} commented on your rec!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'post_tag':
    body = f'{request.user.name} @{request.user.username} has a rec for you!'
    post = Post.objects.get(pk=post_id)
    created_by = post.created_by
    recipient = User.objects.get(pk=recipient_id)
    created_for = recipient
  elif type_of_notification == 'new_follow':
    body = f'{request.user.name} @{request.user.username} followed you!'
    followed_user = User.objects.get(pk=recipient_id)
    created_for = followed_user
  elif type_of_notification == 'new_chat':
    body = f'{request.user.name} @{request.user.username} started a chat with you!'
    chat_recipient = User.objects.get(pk=recipient_id)
    created_for = chat_recipient

  notification = Notification.objects.create(
    body = body,
    created_by = created_by,
    type_of_notification = type_of_notification,
    post_id = post_id,
    created_for = created_for
  )

  return notification