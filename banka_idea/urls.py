# Ссылки для использования views
from django.urls import path, include

from banka_idea import views
from banka_idea.views import Register

urlpatterns = [

    path('get_idea/filter_random/', views.filter_idea_random, name="get-idea-filter-random"),

    path('get_idea/<int:pk>/dislike_idea/', views.dislike_idea, name="idea-dislike"),
    path('get_idea/like_idea/', views.like_idea, name="idea-like"),
    path('get_idea/', views.get_idea_title, name="get-idea-title"),
    path('create_idea/', views.create_idea, name="create-idea"),


    # Изменение идеи
    path('users/profile/<int:pk>/update', views.update_user_idea, name="idea-change"),
    # Удаление идеи
    path('users/profile/<int:pk>/delete', views.delete_user_idea, name="idea-delete"),


    # auth
    path('users/profile/change/', views.change_user, name="user-change"),
    path('users/profile/', views.user_profile, name="user-profile"),
    path('users/register/', Register.as_view(), name="register"),
    path('users/', include('django.contrib.auth.urls')),

    path('', views.main, name="main"),
]