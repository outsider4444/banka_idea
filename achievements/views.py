from django.shortcuts import render

# Create your views here.
from achievements.models import Achievment, UsersAchievments


def add_achievments_to_user(user):
    ac_list = Achievment.objects.all()
    for ac in ac_list:
        UsersAchievments.objects.create(achievment=ac, user=user, status=False)


def get_user_achievments_locked(user):
    achivments_list = UsersAchievments.objects.filter(user=user).filter(status=False)
    return achivments_list


def get_user_achievments_unlocked(user):
    achivments_list = UsersAchievments.objects.filter(user=user).filter(status=True)
    return achivments_list


def add_base_achivement(user, name, parametr=1, condition=None):
    achiv = Achievment.objects.get(name=name)
    if achiv not in get_user_achievments_locked(user):
        add_achievments_to_user(user)
    locked_achiev = UsersAchievments.objects.filter(user=user).get(achievment__name=name)
    print(locked_achiev)
    # Условие - специальное обозначение для того чтобы отличать "уникальные" достижения от простых
    if condition is None:
        if locked_achiev.users_score == achiv.count_to_unlock:
            locked_achiev.status = True
            locked_achiev.save()
        else:
            locked_achiev += parametr