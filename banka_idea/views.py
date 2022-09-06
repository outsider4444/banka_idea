import random

from django.shortcuts import render
from .models import Idea

# Create your views here.

# Настройки представлений для проекта

def list_idea(request):
    list = Idea.objects.all()
    context = {"list" : list}
    return render(request,"test.html", context)

def Random_idea(request):
    #idea = Idea.objects.get(id=random.randint(1,3))
    idea = Idea.objects.order_by('?').first()
    idea_post = Idea
    if request.method == "POST":
        idea_post.name = request.POST.get("name")
        idea_post.description = request.POST.get("description")
        idea_post.save()
    context = {"idea" : idea}
    return render(request,"test.html", context)


