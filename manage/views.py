from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
def manage(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))
        if user.permission == 'admin':
            return render(req, "manage.html", {'user': user})
        else:
            messages.info(req, '관리자가 아닙니다.')
            return redirect('home:index')
    else:
        messages.info(req, '로그인 후 이용하세요.')
        return redirect("home:index")
