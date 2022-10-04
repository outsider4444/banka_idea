from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_chat_list, name="chat-list"),
    path("start_chat/<int:pk>", views.start_chat_to_user, name="start-chat"),
    path("<slug:slug>/", views.chat, name="chatting"),

]