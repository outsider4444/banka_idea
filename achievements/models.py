from django.db import models

# Create your models here.
from banka_idea.models import User


class Achievment(models.Model):
    name = models.CharField("Название", max_length=100)
    image = models.ImageField("Фото", upload_to='achievements')
    description = models.CharField("Описание", max_length=100)
    count_to_unlock = models.IntegerField("Очки для открытия", default=0, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class UsersAchievments(models.Model):
    achievment = models.ForeignKey(Achievment, on_delete=models.CASCADE, verbose_name="Достижение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    users_score = models.IntegerField("Очки пользователя", default=0)
    status = models.BooleanField("Статус", default=False)

    def __str__(self):
        return f'{self.user.username} | {self.achievment.name}'

    class Meta:
        verbose_name = "Пользовательское достижение"
        verbose_name_plural = "Пользовательские достижения"
