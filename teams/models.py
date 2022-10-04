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

# todo Нужен ли секретный код для подключения к чату/группе
class Team(models.Model):
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='blabla/avatar', blank=True, null=True)
    description = RichTextUploadingField()
    idea = models.ForeignKey(Idea, on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField(UserTags, blank=True)
    status = models.BooleanField(default=False, verbose_name="Укомплектована")
    slug = models.SlugField("Код доступа", max_length=50, unique=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return self.name


class UsersInTeams(models.Model):
    """Пользователи в командах"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    capitan = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Человек в команде"
        verbose_name_plural = "Люди в командах"

    def __str__(self):
        return f'{self.user} в команде {self.team} Капитан: {self.capitan}'


class Message(models.Model):
    room = models.ForeignKey(Team, related_name="message", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="message", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ('date_added',)

# todo Написать бан пользователя
