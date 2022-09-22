from django.contrib import admin

# Register your models here.
from achievements.models import UsersAchievments, Achievment

admin.site.register(Achievment)
admin.site.register(UsersAchievments)