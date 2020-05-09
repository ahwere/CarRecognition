from django.urls import path, include
from manage import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'manage'
urlpatterns = [
    path("", views.manage, name="manage"),
    path("reaAllUser/", views.reaAllUser, name="reaAllUser"),
    path("rea/", views.reaOneUser, name="reaOneUser"),
]