from django.shortcuts import render

# Create your views here.
from achievements.models import Achievment, UsersAchievments


def get_user_achievments(user):
    achivments_list = UsersAchievments.objects.filter(user=user)
    return achivments_list


def add_base_achivement(user, name):
    achiv = Achievment.objects.get(name=name)
    if achiv in get_user_achievments(user):
        pass
    else:
        UsersAchievments.objects.create(achiev=achiv, user=user)
