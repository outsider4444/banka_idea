from django.urls import path, include

from . import views

urlpatterns = [

    path('<int:pk>/leave/', views.team_leave, name="leave-team"),
    path('<int:pk>/update/', views.team_update, name="update-team"),
    path('create_new_team/', views.create_team, name="create-team"),
    path('my_teams/', views.my_teams_list, name="my-teams"),
    path('teams_list/', views.teams_list, name="teams-list"),

]