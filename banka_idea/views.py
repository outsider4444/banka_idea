from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import View

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


# Главное меню
def main(request):
    context = {}
    return render(request, "main.html", context)


# Получение идеи
def get_idea_title(request):
    tags_idea = IdeaTags.objects.all()
    context = {
        "tags_idea":tags_idea,
    }
    return render(request, "ideas/get_idea.html", context)


# Получение новых идей
def get_new_idea(request):
    searched_idea = UserIdeaLike.objects.filter(user=request.user)
    list_idea = Idea.objects.order_by('?').first()
    context = {
        "list_idea" : list_idea,
    }
    return render(request, "ideas/get_idea.html", context)


# Идеи пользователя
def list_user_ideas(request):
    user = request.user
    list = Idea.objects.filter(user=user)
    context = {
        "list": list,
    }
    return render(request, "user_ideas.html", context)


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
