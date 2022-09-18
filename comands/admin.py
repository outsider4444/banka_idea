from django.contrib import admin

# Register your models here.
from comands.models import Comand, ComandTags, UsersInComands

admin.site.register(Comand)
admin.site.register(ComandTags)
admin.site.register(UsersInComands)