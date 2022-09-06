from django.shortcuts import render

# Create your views here.

# Настройки представлений для проекта
from banka_idea.forms import IdeaForm
from banka_idea.models import Idea


def list_idea(request):
    list_idea = Idea.objects.order_by('?').first()
    form = IdeaForm()
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = IdeaForm()

    context = {"list_idea": list_idea}
    return render(request,"test.html", context)