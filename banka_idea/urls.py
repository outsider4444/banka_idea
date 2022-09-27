# Ссылки для использования views
from django.urls import path, include

from banka_idea import views
from banka_idea.views import Register

from django.views.decorators.cache import cache_page

urlpatterns = [
    # Список
    path('ideas/list/<int:pk>/tags/', views.tags_search, name="tags-search"),
    path('ideas/list/filter/', views.get_list_idea_filter, name="get-idea-list-filter"),
    path('ideas/list/', views.get_idea_list_title, name="get-idea-list"),

    # Банка
    path('ideas/<int:pk>/dislike_idea/', views.dislike_idea, name="idea-dislike"),
    path('ideas/<int:pk>/like_idea/', views.like_idea, name="idea-like"),
    path('ideas/filter_random/<int:pk>/', views.delete_idea_random, name="delete-idea-random"),
    path('ideas/filter_random/', views.filter_idea_random, name="get-idea-filter-random"),
    path('ideas/create_idea/', views.create_idea, name="create-idea"),
    path('ideas/', views.get_idea_random_title, name="get-idea-title"),

    path('about_page/', views.about_page, name="about-page"),

    # Ответы к идеям

    path('users/profile/solution/<int:pk>/best/', views.set_best_solution, name="solution-best"),
    path('users/profile/solution/<int:pk>/delete/', views.solution_delete, name="solution-delete"),
    path('users/profile/solution/<int:pk>/', views.solution_update, name="solution-update"),
    path('users/profile/<int:pk>/add_solution/', views.add_solution_to_idea, name="solution-add"),

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
    # path('', cache_page(60)(views.main), name='main'),
]