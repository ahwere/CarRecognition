from django.shortcuts import render,redirect
from home.models import Profile
from django.contrib import auth
from django.contrib import messages
# Create your views here.

def statistic(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user_name = Profile.objects.get(user=auth.get_user(req))

        return render(req, "statistic_Service.html",{'user_name':user_name})
    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')

def stat(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user_name = Profile.objects.get(user=auth.get_user(req))

        cctv = req.POST['cctv']
        context = {
            'cctv': cctv,
            'user_name': user_name
        }
        return render(req, "statistic_Service.html", context)

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')
