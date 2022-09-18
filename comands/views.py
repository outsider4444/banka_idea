from django.shortcuts import render

from banka_idea.admin import User
from .models import Comand, ComandTags, UsersInComands


# Create your views here.
# todo Поиск по тегам команд
# todo Поиск команд


def comands_title(request):
    comands_list = Comand.objects.all()


def my_comands_list(request):
    cooperators = UsersInComands.objects.all()
    user_in_comands = UsersInComands.objects.filter(user=request.user)
    # print(comands.comand.name)
    context = {
        'comands_list': user_in_comands,
        'cooperators': cooperators,
    }
    return render(request, "comands/my_comands.html", context)


def comand_info(request):
    pass


def create_command(request):
    pass


def add_comand(request):
    pass


def leave_command(request):
    pass


def delete_command(request):
    pass


