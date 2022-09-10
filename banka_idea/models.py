from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models


# Модели для базы данных
class User(AbstractUser):
    avatar = models.ImageField(upload_to=f'user/avatar', blank=True, null=True)
    rating = models.PositiveIntegerField(default=0)


class IdeaTags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'


class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ideas", blank=True, null=True)
    tags = models.ManyToManyField(IdeaTags, related_name="ideas", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Идея"
        verbose_name_plural = 'Идеи'


class Solution(models.Model):
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/solutions/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = 'Решения'


class UserIdeaLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    checked_idea = models.BooleanField(default=False)
    # favorite?
    # Статусы (взял, не взял, выполнил и тд) ?

    def __str__(self):
        return f'{self.user.username} взял {self.idea.name}. Статус: {self.checked_idea}'

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = 'Лайки'

