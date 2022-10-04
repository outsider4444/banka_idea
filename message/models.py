from django.db import models

# Create your models here.
from banka_idea.models import User


class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name="first_messager", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="second_messager", on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)  # Сунуть имя собеседника + имя пользователя + message

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Message(models.Model):
    room = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)