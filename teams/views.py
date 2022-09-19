from django.db.models import Q
from django.shortcuts import render, redirect

from banka_idea.admin import User
from .forms import TeamCreateForm
from .models import Team, TeamTags, UsersInTeams


# Create your views here.
# todo Поиск по тегам команд
# todo Поиск команд


def teams_list(request):
    team_list = Team.objects.filter(status=False).exclude(capitan=request.user)
    users_in_teams = UsersInTeams.objects.exclude(user=request.user)
    context = {
        "team_list": team_list,
        "users_in_teams": users_in_teams
    }
    return render(request, "teams/team_list.html", context)


def my_teams_list(request):
    cooperators = UsersInTeams.objects.all()
    teams_list = UsersInTeams.objects.filter(user=request.user)
    context = {
        'teams_list': teams_list,
        'cooperators': cooperators,
    }
    return render(request, "teams/my_teams.html", context)


def add_to_team(request, pk):
    pass


def create_team(request):
    form = TeamCreateForm()
    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.capitan = request.user
            obj.save()
            # Добавление чела в команду
            UsersInTeams.objects.create(team=obj,user=request.user,)
            return redirect('user-profile')
        else:
            print(form.errors)
    context = {
        "form":form,
    }
    return render(request, "teams/team_create.html", context)


def team_info(request):
    pass


def team_leave(request):
    pass


def team_update(request, pk):
    updated_team = Team.objects.get(id=pk)
    form = TeamCreateForm(instance=updated_team)
    users_in_team = UsersInTeams.objects.filter(team=updated_team)
    # users_in_team_ids = UsersInTeams.objects.filter(team=updated_team).values(id)
    # print(users_in_team_ids)
    if request.method == "POST":
        team_users = request.POST.getlist('users_in_team')
        print(team_users)
        for team in team_users:
            users_to_delete = users_in_team.exclude(user_id=int(team))

        users_to_delete.delete()
        print(users_to_delete)
        # user_names = [x.user.username for x in users_in_team]
        # user_ids = []
        # for x in user_names:
        #     user_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print()
        #     print(user_ids)
        # for team in user_ids:
        #     UsersInTeams.delete(id=team)

    context = {
        "form":form,
        "users_in_team":users_in_team
    }
    return render(request, 'teams/team_update.html', context)


def team_delete(request):
    pass


def delete_user_from_team(request):
    pass
