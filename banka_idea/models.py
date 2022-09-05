from django.db import models

# Модели для базы данных


class Idea(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)

