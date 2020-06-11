from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from home.models import Profile
from recognition.models import Cctv, CctvLog
from django.contrib import auth
from django.contrib import messages
from django.core import serializers
from home.models import UserLog

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

            if (start_time > end_time):
                messages.info(req, "검색 시간을 확인해주세요.")
                return redirect("recognition:recognition")

            filter_cctv = Cctv.objects.filter(location=location, start_time__lte=start_time).order_by('start_time')

            if bool(filter_cctv) == False:
                cctv_log = []
                video_link = []
            else:
                cctv_log = CctvLog.objects.filter(cctv_id=filter_cctv[0].id, appearance_time__gte=start_time,
                                                  appearance_time__lte=end_time).order_by('appearance_time')

                video_link = filter_cctv[0].video_link.split("static/")[1]
                time1 = int(start_time[17]) * 10
                time2 = int(start_time[18])
                time3 = time1 + time2
                time4 = time3 - filter_cctv[0].start_time.second

                time5 = int(end_time[17]) * 10
                time6 = int(end_time[18])
                time7 = time5 + time6
                etime = time7

                if not cctv_log:
                    messages.info(req, "검색된 데이터가 존재하지 않습니다.")
                else:
                    user_log = UserLog(user = cur_user, search_time = start_time, end_time = end_time, cctv_id = filter_cctv[0])
                    user_log.save()

                return render(req, "recog_Service.html",
                              {'user': user, 'cctv_log': cctv_log, 'cctv': cctv_list, 'count': range(cctv.count()),
                               'date': date, 'video_link': video_link, 'stime': time4, 'etime': time7})

            return render(req, "recog_Service.html",
                          {'user': user, 'cctv_log': cctv_log, 'cctv': cctv_list, 'count': range(cctv.count()),
                           'date': date, 'video_link': video_link})

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
