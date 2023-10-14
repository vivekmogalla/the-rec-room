import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    archived = models.BooleanField(default=False)
    archived_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    
    def modified_at_formatted(self):
       return timesince(self.created_at)

    def get_users(self):
        return "\n >> \n".join([user.email for user in self.users.all()])

    def __str__(self):
        return (
            f"({self.created_at:%y-%m-%d %H:%M})"
        )


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, null=True)
    body = models.TextField()

    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    
    def created_at_formatted(self):
       return timesince(self.created_at)

    def __str__(self):
        return (
            f"{self.created_by} >> "
            f"{self.sent_to} | "
            f"({self.created_at:%y-%m-%d %H:%M})"
        )