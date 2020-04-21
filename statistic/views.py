from django.shortcuts import render

# Create your views here.

def statistic(req):
    return render(req, "statistic_Service.html")

def stat(req):
    cctv = req.POST['cctv']
    context = {'cctv': cctv}
    return render(req, "statistic_Service.html", context)