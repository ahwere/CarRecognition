from django.shortcuts import render, redirect
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

        if req.method == 'POST':
            location = req.POST['location']
            start_time = req.POST['start_time']
            end_time = req.POST['end_time']

            filter_cctv = Cctv.objects.filter(location=location, start_time__lte=start_time).order_by('start_time')

            if bool(filter_cctv) == False:
                cctv_log = []
            else:
                # cctv_log = CctvLog.objects.select_related().filter(cctv_id=filter_cctv[0].id, appearance_time__gte=start_time,
                #                                   appearance_time__lte=end_time).order_by('appearance_time')

                cctv_log = CctvLog.objects.filter(cctv_id=filter_cctv[0].id, appearance_time__gte=start_time,
                                                  appearance_time__lte=end_time).order_by('appearance_time')
                brand_arr = []
                brand_dic = {}
                submit_arr = []

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

        return render(req, "statistic_Service.html",
                      {'user': user, 'cctv': cctv_list, 'count': range(cctv.count()),
                       'dataset': submit_arr})

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')
