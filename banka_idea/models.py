from django.db import models

# Create your models here.
# Модели для базы данных
# Для обновления:
# python manage.py makemigrations
# python manage.py migrate


class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def str(self):
        return self.name