from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def recognition(req):
    return render(req, "recog_Service.html")

def recog(req):
    cctv = req.POST['cctv']
    context = {'cctv': cctv}
    return render(req, "recog_Service.html", context)