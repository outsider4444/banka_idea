from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from banka_idea.admin import User
from banka_idea.models import Idea


class TeamTags(models.Model):
    name = models.CharField(max_length=50)


class Team(models.Model):
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='blabla/avatar', blank=True, null=True)
    description = RichTextUploadingField()
    idea = models.ForeignKey(Idea, on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField(TeamTags, blank=True)
    capitan = models.ForeignKey(User, on_delete=models.PROTECT, to_field='username', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="Укомплектована")

    def __str__(self):
        return self.name


class UsersInTeams(models.Model):
    """Пользователи в командах"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f'{self.user} в команде {self.team}'


# todo Написать бан пользователя