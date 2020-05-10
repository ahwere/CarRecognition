from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile
from django.http import HttpResponseRedirect, JsonResponse
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


def reaAllUser(req):
    context = Profile.objects.all().values()

    return JsonResponse(list(context), safe=False)


def reaOneUser(req):
    result = Profile.objects.filter(id=req.GET['id']).values()

    return JsonResponse(list(result), safe=False)


def delUser(req):
    qs = User.objects.filter(id=req.GET['id'])
    qs.delete()
    context = {
        'data':'성공'
    }
    return JsonResponse(context)
