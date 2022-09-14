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
    achivments_list = UsersAchievments.objects.filter(user=user).filter(achievment__name=name)
    if not achivments_list.filter(achievment__name=achiv.name).exists():
        add_achievments_to_user(user)
    if achivments_list.filter(status=True).get(achievment__name=achiv.name):
        pass
    elif achivments_list.filter(status=False).get(achievment__name=achiv.name):
        print("в списке заблокированных")
        locked_achiv = achivments_list.filter(status=False).get(achievment__name=achiv.name)
        print(locked_achiv)
        # Условие - специальное обозначение для того чтобы отличать "уникальные" достижения от простых
        if condition is None:
            if locked_achiv.users_score == achiv.count_to_unlock:
                locked_achiv.status = True
                locked_achiv.save()
            else:
                locked_achiv += parametr
