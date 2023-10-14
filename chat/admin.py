from django.contrib import admin

from .models import Chat, ChatMessage

class ChatAdmin(admin.ModelAdmin):
    # fields = ['users', 'dollar_amount']
    list_display = ('get_users', '__str__')

admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMessage)
