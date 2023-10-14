import uuid

from django.db import models

from account.models import User
from post.models import Post

class Notification(models.Model):
  NEW_FOLLOW = 'new_follow'
  NEW_CHAT = 'new_chat'
  POST_LIKE = 'post_like'
  POST_COMMENT = 'post_comment'
  POST_TAG = 'post_tag'

  CHOICES_TYPE_OF_NOTIFICATION = (
    (NEW_FOLLOW, 'New follow'),
    (NEW_CHAT, 'New chat'),
    (POST_LIKE, 'Post like'),
    (POST_COMMENT, 'Post comment'),
    (POST_TAG, 'Post tag')
  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  body = models.TextField(blank=True)
  is_read = models.BooleanField(default=False)
  type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
  created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)
  created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ('created_at',)

  def __str__(self):
    return "{} @ {} | {}".format(self.type_of_notification, self.created_for, self.created_at)

  def __str__(self):
    return (
      f"{self.get_type_of_notification_display()} @ "
      f"{self.created_for} "
      f"({self.created_at:%y-%m-%d %H:%M})"
    )
