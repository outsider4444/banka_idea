from django.db import models

# Create your models here.
from banka_idea.admin import User


class Report(models.Model):
    user = models.ForeignKey(User, related_name="report_owner", on_delete=models.CASCADE, verbose_name="Жалоба от")
    reported_user = models.ForeignKey(User, related_name="reported_user", on_delete=models.CASCADE, verbose_name="Жалоба на")
    message = models.TextField("Описание")
    image = models.ImageField(upload_to='reports/', blank=True, null=True, verbose_name="Изображение")

    def __str__(self):
        return f'Жалоба от {self.user} на пользователя {self.reported_user}'

    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"