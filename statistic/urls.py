from django.urls import path
from . import views

urlpatterns = [
    path("", views.statistic, name="statistic"),
]