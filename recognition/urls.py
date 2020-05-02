from django.urls import path
from . import views

urlpatterns = [
    path("", views.recognition, name="recognition"),
    path("recog/", views.recog, name='recog'),
]