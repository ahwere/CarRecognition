from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import Profile
from django.contrib import auth
from django.contrib import messages
from django.core import serializers
from car.models import Car
from recognition.models import Cctv, CctvLog
from django.db.models import Count, Q
from django.db.models import Subquery


# Create your views here.

def statistic(req):
    cur_user = req.user
    cctv = Cctv.objects.all()
    cctv_list = serializers.serialize('json', cctv)

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        return render(req, "statistic_Service.html", {'user': user, 'cctv': cctv_list, 'count': range(cctv.count())})
    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')


def stat(req):
    cur_user = req.user
    cctv = Cctv.objects.all()
    cctv_list = serializers.serialize('json', cctv)

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))
        date = {}
        brand_arr = []
        brand_dic = {}
        submit_arr = []

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

            # print(location)

            filter_cctv = Cctv.objects.filter(location=location, start_time__lte=start_time).order_by('start_time')

            if bool(filter_cctv) == False:
                cctv_log = []
                return redirect('statistic:statistic')

            else:
                cctv_log = CctvLog.objects.filter(cctv_id=filter_cctv[0].id, appearance_time__gte=start_time,
                                                  appearance_time__lte=end_time).order_by('appearance_time')

                for i in cctv_log:
                    brand_arr.append(i.car_model.brand)

                for i in brand_arr:
                    try: brand_dic[i] += 1
                    except: brand_dic[i] = 1

                for i in brand_dic.keys():
                    temp_dic = {}
                    temp_dic['brand'] = i
                    temp_dic['car_count'] = brand_dic[i]
                    submit_arr.append(temp_dic)

            if not cctv_log:
                messages.info(req, "검색된 데이터가 존재하지 않습니다.")

        return render(req, "statistic_Service.html", {'user': user, 'cctv': cctv_list, 'count': range(cctv.count()), 'dataset': submit_arr, 'date': date})

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')
