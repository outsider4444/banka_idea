from django.contrib import admin

# Register your models here.
from notifications.models import Notifications


admin.site.register(Notifications)
