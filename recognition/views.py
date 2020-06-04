from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from home.models import Profile
from recognition.models import Cctv, CctvLog
from django.contrib import auth
from django.contrib import messages
from django.core import serializers
# Create your views here.

def recognition(req):
    cur_user = req.user
    cctv = Cctv.objects.all()
    cctv_list = serializers.serialize('json', cctv)

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        return render(req, "recog_Service.html", {'user': user, 'cctv': cctv_list, 'count': range(cctv.count())})

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect("home:index")

def recog(req):
    cur_user = req.user
    cctv = Cctv.objects.all()
    cctv_list = serializers.serialize('json', cctv)

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))
        date = {}

        if req.method == 'POST':
            location = req.POST['location']
            start_time = req.POST['start_time']
            end_time = req.POST['end_time']

            date['location'] = location
            date['start_time'] = start_time
            date['end_time'] = end_time

            filter_cctv = Cctv.objects.filter(location=location, start_time__lte=start_time).order_by('start_time')

            print(filter_cctv[0].video_link)

            if bool(filter_cctv) == False:
                cctv_log = []
            else:
                cctv_log = CctvLog.objects.filter(cctv_id=filter_cctv[0].id, appearance_time__gte=start_time,
                                                  appearance_time__lte=end_time).order_by('appearance_time')

            return render(req, "recog_Service.html", {'user': user, 'cctv_log': cctv_log, 'cctv': cctv_list, 'count': range(cctv.count()), 'date': date})

        return render(req, "recog_Service.html", {'user': user, 'cctv': cctv_list, 'count': range(cctv.count())})

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect("home:index")


def recogTime(req):

    x = req.GET['time']

    context = {
        'data': x
    }
    return JsonResponse(context)
