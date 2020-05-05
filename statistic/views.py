from django.shortcuts import render,redirect
from home.models import Profile
from django.contrib import auth
# Create your views here.

def statistic(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user_name = Profile.objects.get(user=auth.get_user(req))

        return render(req, "statistic_Service.html",{'user_name':user_name})
    else:
        return redirect('home:index')

def stat(req):
    cctv = req.POST['cctv']
    context = {'cctv': cctv}
    return render(req, "statistic_Service.html", context)