from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from banka_idea.admin import User
from banka_idea.models import Idea, UserTags


# class TeamTags(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


class Team(models.Model):
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='blabla/avatar', blank=True, null=True)
    description = RichTextUploadingField()
    idea = models.ForeignKey(Idea, on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField(UserTags, blank=True)
    status = models.BooleanField(default=False, verbose_name="Укомплектована")

    def __str__(self):
        return self.name


class UsersInTeams(models.Model):
    """Пользователи в командах"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    capitan = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} в команде {self.team} Капитан: {self.capitan}'


# todo Написать бан пользователя