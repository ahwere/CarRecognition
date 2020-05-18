from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.
def manage(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        if user.permission == 'admin':

            if req.method == 'POST':
                uploaded_file = req.FILES['document']
                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name, uploaded_file)
                url = fs.url(name)
                return render(req, "manage.html", {'user': user, 'url':url})
            else:
                return render(req, "manage.html", {'user': user})
        else:
            messages.info(req, '관리자가 아닙니다.')
            return redirect('home:index')
    else:
        messages.info(req, '로그인 후 이용하세요.')
        return redirect("home:index")



        print(uploaded_file.size)
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

