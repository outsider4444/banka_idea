from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import View

from banka_idea.forms import CustomUserCreationForm
from banka_idea.models import Idea


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
def get_idea(request):
    context = {}
    if request.method == "POST":
        list_idea = Idea.objects.order_by('?').first()
        context = {"list_idea": list_idea}
        return render(request, "ideas/get_idea.html", context)
    return render(request, "ideas/get_idea.html", context)


def list_user_ideas(request):
    user = request.user
    list = Idea.objects.filter(user=user)
    context = {"list":list}

    return render(request, "user_ideas.html", context)


# Создание новой идеи
def create_idea(request):
    form = Idea()
    user = request.user
    if request.method == 'POST':
        form.name = request.POST.get("name")
        form.description = request.POST.get("description")
        if user.is_authenticated:
            form.user = user
        form.save()
    context = {
        "form": form,
    }
    return render(request, "ideas/create_new_idea.html", context)
