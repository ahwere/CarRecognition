from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from recognition.models import Cctv
# Create your views here.
def manage(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        if user.permission == 'admin':
            qs = Cctv.objects.all()
            if req.method == 'POST':
                uploaded_file = req.FILES.get('video')
                if uploaded_file==None:
                    messages.info(req, "잘못된 파일 형식입니다.")
                    return render(req, "manage.html", {'user': user, 'qs': qs})
                else:
                    print(len(uploaded_file.name))
                    ext=uploaded_file.name[len(uploaded_file.name)-3:len(uploaded_file.name)]
                    if ext != 'mp4' and ext!='wmv' and ext!='mkv' and ext!='wmv' and ext!='avi' and ext!='MOV' and ext!='FLV':
                        messages.info(req,"잘못된 파일 형식입니다.")
                        return render(req, "manage.html", {'user': user, 'qs': qs})


                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name, uploaded_file)
                url = fs.url(name)
                messages.info(req, "동영상이 업로드 되었습니다.")
                return render(req, "manage.html", {'user': user, 'url':url, 'qs':qs})
            else:
                return render(req, "manage.html", {'user': user, 'qs':qs})
        else:
            messages.info(req, '관리자가 아닙니다.')
            return redirect('home:index')
    else:
        messages.info(req, '로그인 후 이용하세요.')
        return redirect("home:index")

    return render(req,'manage.html')

def reaAllUser(req):
    context = []
    temp = {}

    page = req.GET.get('page',1)

    temp_profile = Profile.objects.all()

    for i in range(len(temp_profile)):
        temp['id'] = temp_profile[i].id
        temp['permission'] = temp_profile[i].permission
        temp['name'] = temp_profile[i].name
        temp['username'] = temp_profile[i].user.username
        context.append(temp)

        temp = {}

    return JsonResponse(context, safe=False)

def delUser(req):
    qs = User.objects.filter(id=req.GET['id'])
    qs.delete()
    context = {
        'data': '회원을 삭제했습니다.'
    }
    return JsonResponse(context)


def grantUser(req):
    qs = Profile.objects.get(id=req.GET['id'])
    qs.permission = req.GET['permission']
    qs.save()

    context = {
        'data' : qs.name + '의 권한을 ' + qs.permission + '(으)로 변경하였습니다.'
    }
    return JsonResponse(context)

def delCctv(req,id):
    qs = Cctv.objects.get(id=id)
    qs.delete()

    return redirect('manage:manage')