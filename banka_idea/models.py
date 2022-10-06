import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models

from pathlib import Path


class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


# Модели для базы данных
class User(AbstractUser):
    avatar = models.ImageField("Аватар", upload_to=f'user/avatar')
    rating = models.PositiveIntegerField("Рейтинг пользователя", default=0)
    first_login = models.DateTimeField(auto_now=True, blank=True, null=True)


class UserTags(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег пользователя"
        verbose_name_plural = "Теги пользователей"


class IdeaTags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'


class Idea(models.Model):
    name = models.CharField("Название", max_length=100)
    description = RichTextUploadingField("Описание", blank=True, null=True)
    date = models.DateTimeField("Дата", auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ideas", blank=True, null=True,
                             verbose_name="Пользователь")
    tags = models.ManyToManyField(IdeaTags, related_name="ideas", blank=True, verbose_name="Теги")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Идея"
        verbose_name_plural = 'Идеи'


class UserIdeaLike(models.Model):
    Choices = ({
        "done": "Выполнено",
        "active": "Не выполнено"
    })
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    checked_idea = models.BooleanField("Статус", default=False)
    date = models.DateTimeField("Дата", auto_now=True, blank=True)

    def __str__(self):
        return f'{self.user.username} взял {self.idea.name}. Статус: {self.checked_idea}'

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = 'Лайки'


class Solution(models.Model):
    text = models.CharField("Текст ответа", max_length=100)
    image = models.ImageField("Изображение", upload_to='solutions', blank=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    url_to_upload = models.URLField("Ссылка", blank=True, null=True)
    description = RichTextUploadingField("Описание", blank=True, null=True)
    date = models.DateTimeField("Дата", auto_now=True, blank=True)
    best_solution = models.BooleanField("Лучший ответ", default=False)

    def __str__(self):
        return f'{self.text} | {self.user.username}'

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = 'Решения'


class News(models.Model):
    name = models.CharField("Заголовок", max_length=255, blank=True, null=True)
    description = RichTextUploadingField("Описание", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    date = models.DateTimeField("Дата", auto_now_add=True)
    image = models.ImageField("Фото",upload_to='news/images', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"