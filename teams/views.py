from django.db.models import Q, Max
from django.shortcuts import render, redirect

from achievements.views import get_user_achievments_unlocked
from banka_idea.admin import User
from banka_idea.models import UserTags
from message.views import check_exist_chat
from notifications.models import Notifications
from .forms import TeamCreateForm
from .models import Team, UsersInTeams, Message


# Create your views here.
# todo Поиск по тегам команд
# todo Поиск команд


def teams_list(request):
    team_list = Team.objects.filter(status=False)
    users_in_teams = UsersInTeams.objects.filter(user=request.user)
    users_not_in_my_team = UsersInTeams.objects.exclude(user=request.user).order_by('-capitan')

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
    cooperators = UsersInTeams.objects.all().order_by('-capitan')
    team_list = UsersInTeams.objects.filter(user=request.user)

    team_list_to_add = Team.objects.filter(status=False)
    users_in_teams = UsersInTeams.objects.filter(user=request.user)

    for team in team_list_to_add:
        for users in users_in_teams:
            if team.id == users.team.id:
                team_list_to_add = team_list_to_add.exclude(id=users.team.id)
    team_list_to_add = team_list_to_add[:5]
    context = {
        'team_list': team_list,
        'cooperators': cooperators,
        'team_list_to_add': team_list_to_add,
    }
    return render(request, "teams/my_teams.html", context)


def add_to_team(request, slug):
    team_to_add = Team.objects.get(slug=slug)

    users_in_team = UsersInTeams.objects.filter(team=team_to_add)
    for user in users_in_team:
        Notifications.objects.create(user=user.user, text=f"Пользователь {request.user} присоеденился к команде {team_to_add.name}")

    UsersInTeams.objects.create(user=request.user, team_id=team_to_add.id, capitan=False)

    return redirect('my-teams')


def create_team(request):
    form = TeamCreateForm()
    if request.method == "POST":
        form = TeamCreateForm(request.POST, request.FILES)
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


def team_detail(request, slug):
    team_name = Team.objects.get(slug=slug)
    users_in_team = UsersInTeams.objects.filter(team__id=team_name.id).order_by('-capitan')

    message_list = Message.objects.filter(room=team_name)

    check_new_user = users_in_team.filter(user=request.user).exists()

    context = {
        "team_name": team_name,
        "users_in_team": users_in_team,
        "message_list": message_list,
        "check_new_user": check_new_user,
    }
    return render(request, "teams/team_detail.html", context)


def team_leave(request, slug):
    team_to_leave = UsersInTeams.objects.filter(user=request.user).get(team__slug=slug)
    team_name = Team.objects.get(name=team_to_leave.team.name)

    teammates = UsersInTeams.objects.filter(team__name=team_name.name).exclude(user=request.user)
    if team_to_leave.capitan:
        teammates = teammates.order_by('-user__rating').first()
        if teammates:
            teammates.capitan = True
            teammates.save()
        else:
            team_name.delete()
    team_to_leave.delete()
    return redirect('my-teams')


def team_update(request, slug):
    updated_team = Team.objects.get(slug=slug)
    form = TeamCreateForm(instance=updated_team)
    users_in_team_now = UsersInTeams.objects.filter(team=updated_team).order_by('-capitan')
    users_in_team_del = UsersInTeams.objects.filter(team=updated_team)
    if request.method == "POST":
        form = TeamCreateForm(request.POST, request.FILES, instance=updated_team)
        team_tags = request.POST.getlist('tags')
        if form.is_valid():
            obj = form.save(commit=False)

            team_users = request.POST.getlist('users_in_team')
            team_capitan = request.POST.get('capitan_team')

            old_cap = UsersInTeams.objects.filter(team__id=updated_team.id).filter(capitan=True)
            new_cap = UsersInTeams.objects.filter(team__id=updated_team.id).get(user__username=team_capitan)

            for cap in old_cap:
                if new_cap != cap.user:
                    cap.capitan = False
                    cap.save()
                new_cap.capitan = True
                new_cap.save()

            for team in team_users:
                for user_to_del in users_in_team_now:
                    if user_to_del.user.id == int(team):
                        users_in_team_del = users_in_team_del.exclude(user_id=int(team))
            if users_in_team_del:
                users_in_team_del.delete()

            obj.tags.clear()

            obj.tags.set(team_tags)
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


# Профиль тиммейта
def user_teammate_profile(request, pk):
    user_teammate = User.objects.get(id=pk)
    user_achievments = get_user_achievments_unlocked(user_teammate)
    user_tags = UserTags.objects.filter(user=user_teammate)
    check_chat = check_exist_chat(request, user_teammate)
    context = {
        "user_teammate": user_teammate,
        "user_tags": user_tags,
        "check_chat": check_chat,
    }
    return render(request, "teams/user_teammate_profile.html", context)
