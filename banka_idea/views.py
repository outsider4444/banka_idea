from django.shortcuts import render

from banka_idea.forms import IdeaForm
from banka_idea.models import Idea

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
        return render(request, "get_idea.html", context)
    return render(request, "get_idea.html", context)


# Создание новой идеи
def create_idea(request):
    form = IdeaForm()
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = IdeaForm()

    context = {"form":form}
    return render(request,"create_new_idea.html", context)