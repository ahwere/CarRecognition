from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from home.models import Profile
from recognition.models import Cctv, CctvLog
from django.contrib import auth
from django.contrib import messages
from django.core import serializers
import json
# Create your views here.

def recognition(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        if req.method == 'POST':
            location = req.POST['location']
            start_time = req.POST['start_time']
            end_time = req.POST['end_time']

            cctv = Cctv.objects.filter(location=location, start_time__lte=start_time).order_by('start_time')
            cctv_logs=[]
            if bool(cctv) == False:
                cctv_logs = []
            else:
                cctv_logs = CctvLog.objects.filter(cctv_id=cctv[0].id, appearance_time__gte=start_time, appearance_time__lte=end_time).order_by('appearance_time').values()
                for temp in cctv_logs:
                    datetemp = temp['appearance_time'].strftime("%Y/%m/%d %H:%M:%S")
                    temp['appearance_time'] = datetemp


            cctv_logjson = json.dumps(list(cctv_logs))

            return render(req, "recog_Service.html", {'user': user, 'cctv_logs': cctv_logjson})

        else:
            return render(req, "recog_Service.html")


    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect("home:index")


def recog(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        cctv = req.POST['cctv']
        context = {
            'cctv': cctv,
            'user': user
        }

        return render(req, "recog_Service.html", context)

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect("home:index")


def recogTime(req):

    x = round(float(req.GET['time']))

    context = {
        'data': x
    }
    return JsonResponse(context)
