from django.shortcuts import render, redirect
import json
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from home.forms import ProfileForm
from django.http import HttpResponse
# Create your views here.

from django.contrib.auth.forms import UserCreationForm
# from home.forms import PostForm

def index(req) :
    context = {

    }

    return render(req, "index.html", context=context)

def login(req):
    # if req.method == 'POST':
    #     something
    #
    # else:
    #     form =
    return render(req, "login.html")

def register(req):
    if req.method == 'POST':
        user_form = UserCreationForm(req.POST)
        profile_form = ProfileForm(req.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # user_form.save()
            # profile_form.save()
            # return redirect('home:index')
            return HttpResponse(profile_form)

        # else:
        #     return HttpResponse(user_form)
    else:
        user_form = UserCreationForm()

    return render(req, "register.html", {'user_form':user_form})

def mypage(req):
    return render(requset, "mypage.html")