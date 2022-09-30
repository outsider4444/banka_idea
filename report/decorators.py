from django.http import HttpResponse
from django.shortcuts import redirect


def active_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_active:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Вы не имеете доступа к данной странице')

    return wrapper_func
