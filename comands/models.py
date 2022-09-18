from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from banka_idea.admin import User
from banka_idea.models import Idea


class ComandTags(models.Model):
    name = models.CharField(max_length=50)


class Comand(models.Model):
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='comands/avatar', blank=True, null=True)
    description = RichTextUploadingField()
    idea = models.ForeignKey(Idea, on_delete=models.PROTECT)
    tags = models.ManyToManyField(ComandTags, blank=True)
    capitan = models.ForeignKey(User, on_delete=models.PROTECT, related_name='capitan')

    def __str__(self):
        return self.name


class UsersInComands(models.Model):
    """Пользователи в командах"""
    comand = models.ForeignKey(Comand, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} в команде {self.comand}'