from django.urls import path, include

from comands import views

urlpatterns = [
    path('my_comands/', views.my_comands_list, name="my-comands"),
]