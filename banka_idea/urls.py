# Ссылки для использования views
from django.urls import path

from banka_idea import views

urlpatterns = [
    path('', views.list_idea, name="list-idea"),
]