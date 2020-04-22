from django.shortcuts import render

# Create your views here.

def statistic(req):
    return render(req, "statistic_Service.html")
