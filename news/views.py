from django.shortcuts import render

# Create your views here.
from news.models import News


def news_list(request):
    news = News.objects.all().order_by("-date")
    # Взять новости за неделю

    context = {
        "news":news
    }
    return render(request, "news/news_list.html", context)