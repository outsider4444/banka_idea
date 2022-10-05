from django.db import models

# Create your models here.
from banka_idea.models import User


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
