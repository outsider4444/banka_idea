from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from banka_idea.models import User
from message.models import Chat, Message


def check_exist_chat(request, pk):
    chats = Chat.objects.filter(
        Q(user1=request.user) &
        Q(user2=pk) |
        Q(user1=pk) &
        Q(user2=request.user)
    )
    if chats.exists():
        return True
    else:
        return False


def get_chat_list(request):
    chats = Chat.objects.filter(
        Q(user1=request.user) |
        Q(user2=request.user)
    )
    context = {
        "chats": chats,
    }
    return render(request, "messages/chat_list.html", context)


def start_chat_to_user(request, pk):
    user1 = request.user
    user2 = User.objects.get(id=pk)
    slug: str = user1.username + user2.username + "message"
    Chat.objects.create(user1=user1, user2_id=user2.id, slug=slug)
    return redirect('chat-list')


def chat(request, slug):
    chat = Chat.objects.get(slug=slug)
    chats = Chat.objects.filter(
        Q(user1=request.user) |
        Q(user2=request.user)
    )
    messages = Message.objects.filter(room=chat)
    context = {
        "chat": chat,
        "chats": chats,
        "messages":messages,
    }
    return render(request, "messages/chat_room.html", context)
