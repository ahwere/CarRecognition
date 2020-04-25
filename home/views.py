from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def index(req) :

    user_name = None

    if req.user.is_anonymous!=True:
        user_name = Profile.objects.get(user=auth.get_user(req))

    return render(req, "index.html", {'user_name':user_name})

def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = auth.authenticate(req, username=username, password=password)

        if user is not None:
            auth.login(req, user)
            return redirect('home:index')
        else:
            messages.info(req, '아이디 혹은 비밀번호가 틀렸습니다.')
            return render(req, "login.html")

    else:
        return render(req, "login.html")

def logout(req):

    auth.logout(req)
    messages.info(req, '로그아웃 되었습니다.')

    return redirect('home:index')

def register(req):
    if req.method == 'POST':
        user_form = UserCreationForm(req.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.get(user=user)
            profile.name = req.POST['name']
            profile.save()

            login_id = User.objects.get(username=profile.user.username)
            auth.login(req, login_id)

            return redirect('home:index')

        else:
            messages.info(req, '중복된 아이디 혹은 비밀번호가 틀렸습니다.')
    else:
        user_form = UserCreationForm()

    return render(req, "register.html", {'user_form':user_form})

def mypage(req):
    return render(req, "mypage.html")