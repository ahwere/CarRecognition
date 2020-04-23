from django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from home.forms import PostForm
# Create your views here.

def index(req) :
    context = {

    }

    return render(req, "index.html", context=context)

def login(req):
    return render(req, "login.html")

def register(req):
    return render(req, "register.html")

def mypage(req):
    return render(req, "mypage.html")