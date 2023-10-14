from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from notification.utils import create_notification

from .models import Chat, ChatMessage
from .serializers import ChatSerializer, ChatDetailSerializer, ChatMessageSerializer


@api_view(['GET'])
def chat_list(request):
    chats = Chat.objects.filter(users__in=list([request.user])).order_by('-modified_at')
    serializer = ChatSerializer(chats, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def chat_detail(request, id):
    print(f'chat detail id: {id}')
    chat = Chat.objects.filter(users__in=list([request.user])).get(pk=id)
    serializer = ChatDetailSerializer(chat)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def chat_get_or_create(request, user_id):
    user = User.objects.get(pk=user_id)
    chats = Chat.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

    if chats.exists():
        chat = chats.first()
    else:
        chat = Chat.objects.create()
        chat.users.add(user, request.user)
        chat.save()
        create_notification(request, 'new_chat', recipient_id=user.id)

    serializer = ChatDetailSerializer(chat)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def chat_send_message(request, id):
    chat = Chat.objects.filter(users__in=list([request.user])).get(pk=id)
    for user in chat.users.all():
        if user != request.user:
            sent_to = user
    message = ChatMessage.objects.create(
        chat=chat,
        body=request.data.get('body'),
        created_by=request.user,
        sent_to=sent_to,
    )

    serializer = ChatMessageSerializer(message)

    return JsonResponse(serializer.data, safe=False)