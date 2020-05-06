from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def manage(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user_name = Profile.objects.get(user=auth.get_user(req))

        return render(req, "manage.html", {'user_name': user_name})
    else:
        messages.info(req, '관리자가 아닙니다.')
        return redirect("home:index")

def reaUserAll(req):
    qs = Profile.objects.all()
    context = {'user_list': qs}

    return render(req,'manage.html', context)