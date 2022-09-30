from django.urls import path, include

from . import views

urlpatterns = [
    path('teammate/<int:pk>/', views.user_teammate_profile, name="teammate-profile"),
    path('<str:slug>/detail/', views.team_detail, name="team-detail"),
    path('<str:slug>/add/', views.add_to_team, name="add-team"),
    path('<str:slug>/leave/', views.team_leave, name="leave-team"),
    path('<str:slug>/update/', views.team_update, name="update-team"),
    path('create_new_team/', views.create_team, name="create-team"),
    path('my_teams/', views.my_teams_list, name="my-teams"),
    path('teams_list/', views.teams_list, name="teams-list"),
]