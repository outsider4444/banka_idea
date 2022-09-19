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


def team_leave(request, pk):
    print(pk)
    team_to_leave = UsersInTeams.objects.filter(user=request.user)
    team_to_leave = team_to_leave.get(id=pk)
    team_name = Team.objects.get(name=team_to_leave.team.name)

    if request.user == team_to_leave.team.capitan:
        pass
        team_to_leave.delete()
        cooperate = UsersInTeams.objects.filter(team__name=team_to_leave.team.name).exclude(user=request.user)
        if cooperate:
            cooperate = cooperate.order_by('-user__rating').first()
            print(cooperate)
            team_name.capitan = cooperate.user
            team_name.save()
    return redirect('my-teams')


def team_update(request, pk):
    updated_team = Team.objects.get(id=pk)
    form = TeamCreateForm(instance=updated_team)
    users_in_team_now = UsersInTeams.objects.filter(team=updated_team)
    users_in_team_del = UsersInTeams.objects.filter(team=updated_team)
    if request.method == "POST":
        form = TeamCreateForm(request.POST, instance=updated_team)
        if form.is_valid():
            obj = form.save(commit=False)

            team_users = request.POST.getlist('users_in_team')
            team_capitan = request.POST.get('capitan_team')

            if obj.capitan != team_capitan:
                new_cap = User.objects.get(username=team_capitan)
                obj.capitan = new_cap

            for team in team_users:
                for user_to_del in users_in_team_now:
                    if user_to_del.user.id == int(team):
                        # print("ТРУ")
                        users_in_team_del = users_in_team_del.exclude(user_id=int(team))

            if users_in_team_del:
                users_in_team_del.delete()

            obj.save()
            return redirect('my-teams')
        else:
            print(form.errors)

    context = {
        "updated_team":updated_team,
        "form":form,
        "users_in_team":users_in_team_now
    }
    return render(request, 'teams/team_update.html', context)


def team_delete(request):
    pass
