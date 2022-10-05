from django.urls import path, include

from notifications import views

urlpatterns = [
    path("get_count_notification/", views.count_new_notifications, name="count-notification"),
    path("<int:pk>/", views.delete_notification, name="delete-notification"),
    path("", views.get_notifications, name="my-notification"),
]