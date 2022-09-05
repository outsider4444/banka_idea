from django.shortcuts import render

# Create your views here.

# Настройки представлений для проекта

def list_idea(request):
    context = {}
    return render(request,"test.html", context)