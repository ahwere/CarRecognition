from django.shortcuts import render, redirect
import json
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from home.forms import PostForm
from django.http import HttpResponse
# Create your views here.

from django.contrib.auth.forms import UserCreationForm

def index(req) :
    context = {

    }

    return render(req, "index.html", context=context)

def login(req):
    if req.method == 'POST':
        something

    else:
        form = 
    return render(req, "login.html")

def register(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            return HttpResponse(form)

    else:
        form = UserCreationForm()

    return render(req, "register.html", {'form':form})

def mypage(req):
    return render(requset, "mypage.html")