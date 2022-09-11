from django.db import models

# Create your models here.
from banka_idea.models import User


class Achievment(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='achievements')
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class UsersAchievments(models.Model):
    achievment = models.ForeignKey(Achievment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | {self.achiev.name}'

    class Meta:
        verbose_name = "Пользовательское достижение"
        verbose_name_plural = "Пользовательские достижения"