from django.urls import path
from . import views

app_name = 'recognition'
urlpatterns = [
    path("", views.recognition, name="recognition"),
    path("recog/", views.recog, name='recog'),
]