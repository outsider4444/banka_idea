from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from banka_idea.models import User


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
