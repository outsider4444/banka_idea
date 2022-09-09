from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from banka_idea.models import Idea, IdeaTags

# Настройки для панели администратора

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    pass


admin.site.register(Idea)
admin.site.register(IdeaTags)