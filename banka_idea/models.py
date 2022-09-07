from django.contrib.auth.models import AbstractUser
from django.db import models


# Модели для базы данных
class User(AbstractUser):
    pass


class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # Лайки?
    # Просмотры?
    # Счетчики?

    def __str__(self):
        return self.name


