# Ссылки для использования views
from django.urls import path

from banka_idea import views

urlpatterns = [
    path('', views.main, name="main"),
    path('get_idea/', views.get_idea, name="get-idea"),
    path('create/', views.create_idea, name="create-idea"),
]