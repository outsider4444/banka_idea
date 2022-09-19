from django.db.models import Q, Max
from django.shortcuts import render, redirect

from banka_idea.admin import User
from .forms import TeamCreateForm
from .models import Team, TeamTags, UsersInTeams


# Create your views here.
# todo Поиск по тегам команд
# todo Поиск команд


def teams_list(request):
    team_list = Team.objects.filter(status=False)
    users_in_teams = UsersInTeams.objects.filter(user=request.user)
    users_not_in_my_team = UsersInTeams.objects.exclude(user=request.user)

    for team in team_list:
        for users in users_in_teams:
            if team.id == users.team.id:
                team_list = team_list.exclude(id=users.team.id)
    context = {
        "team_list": team_list,
        "users_not_in_team": users_not_in_my_team,
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
    team_to_add = Team.objects.get(id=pk)
    UsersInTeams.objects.create(user=request.user, team_id=team_to_add.id, capitan=False)
    return redirect('my-teams')


def create_team(request):
    form = TeamCreateForm()
    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # Добавление чела в команду
            UsersInTeams.objects.create(team=obj, user=request.user, capitan=True)
            return redirect('my-teams')
        else:
            print(form.errors)
    context = {
        "form": form,
    }
    return render(request, "teams/team_create.html", context)


def team_info(request, pk):
    team_name = Team.objects.get(id=pk)
    return redirect('my-teams')


def team_leave(request, pk):
    print(pk)
    team_to_leave = UsersInTeams.objects.filter(user=request.user).get(id=pk)
    team_name = Team.objects.get(name=team_to_leave.team.name)

    teammates = UsersInTeams.objects.filter(team__name=team_name.name).exclude(user=request.user)
    print(teammates)
    if team_to_leave.capitan:

        teammates = teammates.order_by('-user__rating').first()
        teammates.capitan = True
        teammates.save()
    team_to_leave.delete()
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

            old_cap = UsersInTeams.objects.filter(team__id=updated_team.id).filter(capitan=True)
            new_cap = UsersInTeams.objects.filter(team__id=updated_team.id).get(user__username=team_capitan)
            print(old_cap)
            for cap in old_cap:
                if new_cap != cap.user:
                    cap.capitan = False
                    cap.save()
                new_cap.capitan = True
                new_cap.save()

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
        "updated_team": updated_team,
        "form": form,
        "users_in_team": users_in_team_now
    }
    return render(request, 'teams/team_update.html', context)


def team_delete(request):
    pass
