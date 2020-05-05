from django.urls import path, include
from home import views

app_name = 'home'

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("mypage/", views.mypage, name="mypage"),
    path("logout/", views.logout, name="logout"),
    path("update/", views.update, name="update"),
    path("dismember/", views.dismember, name="dismember"),
    path("manage/", views.manage, name="manage"),
]