from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Модели для базы данных
class User(AbstractUser):
    avatar = models.ImageField(upload_to='media/user/avatar/', blank=True, null=True)
    rating = models.IntegerField(default=0)


class IdeaTags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ideas", blank=True, null=True)
    tags = models.ManyToManyField(IdeaTags, related_name="ideas", blank=True)

    def __str__(self):
        return self.name


class Solution(models.Model):
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/solutions/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, blank=True)


class UserIdeaLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    checked_idea = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} взял {self.idea.name}. Статус: {self.checked_idea}'
    # favorite?
    # liked ?
    # Статусы (взял, не взял, выполнил и тд) ?
