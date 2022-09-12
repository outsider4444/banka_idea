# Ссылки для использования views
from django.urls import path, include

from banka_idea import views
from banka_idea.views import Register

urlpatterns = [

    path('get_idea/<int:pk>/dislike_idea/', views.dislike_idea, name="idea-dislike"),
    path('get_idea/<int:pk>/like_idea/', views.like_idea, name="idea-like"),
    path('get_idea/filter_random/', views.filter_idea_random, name="get-idea-filter-random"),
    path('get_idea/', views.get_idea_title, name="get-idea-title"),
    path('create_idea/', views.create_idea, name="create-idea"),



    path('users/profile/solution_list/<int:pk>/', views.solution_update, name="solution-update"),
    path('users/profile/solution_list/', views.solution_list, name="solution-list"),
    # Добавление ответа к идее
    path('users/profile/<int:pk>/add_solution/', views.add_solution_to_idea, name="add-solution"),
    # Изменение идеи
    path('users/profile/<int:pk>/update/', views.update_user_idea, name="idea-change"),
    # Удаление идеи
    path('users/profile/<int:pk>/delete/', views.delete_user_idea, name="idea-delete"),

    # Поиск
    path('search/', views.search_results, name="search"),


    # auth
    path('users/profile/change/', views.change_user, name="user-change"),
    path('users/profile/', views.user_profile, name="user-profile"),
    path('users/register/', Register.as_view(), name="register"),
    path('users/', include('django.contrib.auth.urls')),

    path('', views.main, name="main"),
]