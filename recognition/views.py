from django.shortcuts import render

# Create your views here.

def recognition(req):
    return render(req, "recog_Service.html")
