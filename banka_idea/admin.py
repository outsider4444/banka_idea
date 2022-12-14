from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from banka_idea.models import Idea, IdeaTags, UserIdeaLike, Solution, UserTags

# Настройки для панели администратора

User = get_user_model()


class IdeaInstanceInline(admin.TabularInline):
    model = Idea


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ['first_login']
    fieldsets = (
        (None, {
            'fields': ('avatar','username', 'email', 'password')
        }),
        ('Личная информация', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Информация', {
            'fields': ('rating', 'first_login')
        }),
        ('Теги', {
            'fields': ('tags',)
        }),
        ('Активный пользователь', {
            'fields': ('is_active',)
        }),
    )


admin.site.register(Idea)
admin.site.register(IdeaTags)
admin.site.register(Solution)
admin.site.register(UserTags)


@admin.register(UserIdeaLike)
class UserIdeaLikeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user', 'idea', 'checked_idea')
        }),
    )

