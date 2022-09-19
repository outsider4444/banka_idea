from django.contrib import admin

# Register your models here.
from .models import Team, TeamTags, UsersInTeams

admin.site.register(Team)
admin.site.register(TeamTags)
admin.site.register(UsersInTeams)