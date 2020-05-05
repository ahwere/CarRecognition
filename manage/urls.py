from django.urls import path, include
from manage import views

app_name = 'manage'
urlpatterns = [
    path("", views.manage, name="manage"),
    path("All/", views.reaUserAll, name='reaUserAll'),
]