from django.urls import path, include

from notifications import views

urlpatterns = [
    path("", views.get_notifications, name="my-notification"),
    path("get_count_notification/", views.count_new_notifications, name="count-notification")
]