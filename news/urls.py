from django.urls import path

from news import views

urlpatterns = [
    path('', views.news_list, name="news-list")
]