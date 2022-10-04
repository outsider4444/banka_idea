from django.contrib import admin

# Register your models here.
from message.models import Message, Chat

admin.site.register(Chat)
admin.site.register(Message)
