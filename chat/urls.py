from django.urls import path

from . import api

urlpatterns = [
    path('', api.chat_list, name='chat_list'),
    path('<uuid:id>/', api.chat_detail, name='chat_detail'),
    path('<uuid:id>/send/', api.chat_send_message, name='chat_send_message'),
    path('<uuid:user_id>/get-or-create/', api.chat_get_or_create, name='chat_get_or_create'),
]
