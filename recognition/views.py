from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from home.models import Profile
from recognition.models import Cctv, CctvLog
from django.contrib import auth
from django.contrib import messages


# Create your views here.

def recognition(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        if req.method == 'POST':
            location = req.POST['location']
            start_time = req.POST['start_time']
            end_time = req.POST['end_time']

            cctv = Cctv.objects.filter(location=location, start_time__gte=start_time).order_by('start_time')

            if bool(cctv) == False:
                cctv_log = []
            else:
                cctv_log = CctvLog.objects.filter(cctv_id=cctv[0].id, appearance_time__gte=start_time, appearance_time__lte=end_time).order_by('appearance_time')

            return render(req, "recog_Service.html", {'user': user, 'cctv_log': cctv_log})

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
