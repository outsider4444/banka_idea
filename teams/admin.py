from django.contrib import admin

# Register your models here.
from .models import Team, UsersInTeams

admin.site.register(Team)
admin.site.register(UsersInTeams)