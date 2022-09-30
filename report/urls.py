from django.urls import path

from report import views

urlpatterns = [
    path('<int:pk>/', views.report_view, name="report-form"),
]