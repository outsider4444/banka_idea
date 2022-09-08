# Ссылки для использования views
from django.urls import path, include

from banka_idea import views
from banka_idea.views import Register

urlpatterns = [
    path('get_idea/force/', views.get_new_idea, name="get-new-idea"),
    path('get_idea/', views.get_idea_title, name="get-idea-title"),
    path('create_idea/', views.create_idea, name="create-idea"),

    # auth
    path('users/ideas', views.list_user_ideas, name="users-ideas"),
    path('users/register', Register.as_view(), name="register"),
    path('users/', include('django.contrib.auth.urls')),

    path('', views.main, name="main"),
]