from django.urls import path
from . import views

app_name = 'statistic'
urlpatterns = [
    path("", views.statistic, name="statistic"),
    path("stat/", views.stat, name="stat"),

    path('test/', views.test, name='test'),
]