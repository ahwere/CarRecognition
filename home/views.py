from django.shortcuts import render

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