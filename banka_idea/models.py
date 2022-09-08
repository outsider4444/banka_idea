from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models


# Модели для базы данных
class User(AbstractUser):
    pass


class IdeaTags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(IdeaTags, related_name="ideas", blank=True, null=True)
    # Лайки?
    # Просмотры?
    # Счетчики?

    def __str__(self):
        return self.name


class UserIdeaLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    checked_idea = models.BooleanField(default=False)
    # favorite?
    # liked ?
    # ЧТО БЛЯТЬ И КАК ВООБЩЕ РЕАЛИЗОВЫВАТЬ, ПОД ТИНДЕР ИЛИ ПОД КАКУЮ ВООБЩЕ ХУЙНЮ?