from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from banka_idea.forms import CustomUserCreationForm, IdeaForm
from banka_idea.models import Idea, IdeaTags, UserIdeaLike


# Регистрация
class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {
            "form": CustomUserCreationForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("main")
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


def user_profile(request):
    users_idea_liked = UserIdeaLike.objects.filter(user=request.user)
    list_user_idea = Idea.objects.filter(user=request.user)
    context = {
        "users_idea_liked": users_idea_liked,
        "list_user_idea": list_user_idea,
    }
    return render(request, "registration/profile.html", context)


# Главное меню
def main(request):
    context = {}
    return render(request, "main.html", context)


# Получение идеи
def get_idea_title(request):
    """Вывод страницы идей"""
    idea_list = Idea.objects.all()
    idea_tag_list = IdeaTags.objects.all()
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list
    }
    return render(request, "ideas/get_idea.html", context)


def filter_idea(request):
    """Фильтрация идей и вывод по 1"""
    check = []
    idea_list = Idea.objects.all()

    # Получение идей пользователя, которые он отметил
    users_checked_idea = UserIdeaLike.objects.filter(user=request.user).filter(checked_idea=True) # последний фильтр под вопросом
    idea_tag_list = IdeaTags.objects.all()

    # Получаем теги из формы
    for tag in idea_tag_list:
        check.append(request.GET.get(tag.name))

    # Фильтруем по тегам
    for tag in check:
        if tag is not None:
            idea_list = idea_list.filter(
                Q(tags__name=tag)
            )
    # Фильтруем по отмеченным идеям
    for checked_idea in users_checked_idea:
        idea_list = idea_list.exclude(id=checked_idea.idea.id)

    # Получение случайной
    new_idea = idea_list.order_by('?').first()
    context = {
        "idea_list": idea_list,
        "idea_tag_list": idea_tag_list,
        "new_idea": new_idea,
    }
    return render(request, "ideas/get_idea.html", context)


def like_idea(request):
    """Добавление идей в избранное"""
    if request.method == "POST":
        idea = request.POST.get("idea_id")
        user = request.user
        print(idea)
        UserIdeaLike.objects.create(idea_id=idea, user=user, checked_idea=True)
    context = {

    }
    return render(request, "ideas/get_idea.html", context)

# def filter_idea(request):
#     check = []
#     idea_list = Idea.objects.all()
#     idea_tag_list = IdeaTags.objects.all()
#     for tag in idea_tag_list:
#         check.append(request.GET.get(tag.name))
#     for tag in check:
#         if tag is not None:
#             idea_list = idea_list.filter(
#                 Q(tags__name=tag)
#             )
#     context = {
#         "idea_list": idea_list,
#         "idea_tag_list": idea_tag_list
#     }
#     return render(request, "ideas/get_idea.html", context)


# Создание новой идеи
def create_idea(request):
    tags_idea = IdeaTags.objects.all()
    form = IdeaForm()
    user = request.user
    if request.method == 'POST':
        form = IdeaForm(request.POST)

        ###
        tags_names = [x.name for x in tags_idea]
        tags_ids = []
        for x in tags_names:
            tags_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print()
            print(tags_ids)
        ###
        if form.is_valid():
            obj = form.save(commit=False)
            # Добавление пользователя к записи если авторизован
            if user.is_authenticated:
                obj.user = user
            obj.save()
            print(obj.user)
            for x in tags_ids:
                obj.tags.add(IdeaTags.objects.get(id=x))
            obj.save()
            # return redirect("create_idea")
        else:
            print(form.errors)
    context = {
        "form": form,
        "tags_idea": tags_idea,
    }
    return render(request, "ideas/create_new_idea.html", context)