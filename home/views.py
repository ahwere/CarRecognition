from django.shortcuts import render

# Create your views here.

def index(req) :
    context = {

    }

    return render(req, "index.html", context=context)