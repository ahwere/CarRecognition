from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from home.models import Profile, UserLog
from recognition.models import CctvLog, Cctv
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.template import RequestContext
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers



def index(req) :

    user_name = None

    if req.user.is_anonymous!=True:
        user_name = Profile.objects.get(user=auth.get_user(req))

    return render(req, "index.html", {'user':user_name})

def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = auth.authenticate(req, username=username, password=password)

        if user is not None:
            auth.login(req, user)
            return redirect('home:index')
        else:
            messages.info(req, '아이디 혹은 비밀번호가 틀렸습니다.')
            return render(req, "login.html")

    else:
        return render(req, "login.html")

def logout(req):

    auth.logout(req)
    messages.info(req, '로그아웃 되었습니다.')

    return redirect('home:index')

def register(req):
    if req.method == 'POST':
        user_form = UserCreationForm(req.POST)
        if user_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.get(user=user)
            profile.name = req.POST['name']
            profile.save()

            login_id = User.objects.get(username=profile.user.username)
            auth.login(req, login_id)

            messages.info(req, '회원가입이 정상적으로 완료되었습니다.')
            return redirect('home:index')

        else:
            messages.info(req, '중복된 아이디 혹은 비밀번호가 틀렸습니다.')
    else:
        user_form = UserCreationForm()

    return render(req, "register.html", {'user_form':user_form})

def mypage(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user = Profile.objects.get(user=auth.get_user(req))

        return render(req, "mypage.html", {'user': user})
    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect("home:index")

def update(req):

    user_name = Profile.objects.get(user=auth.get_user(req))
    context= {'user_name':user_name}

    if req.method == "POST":
        current_password = req.POST.get("origin_password")
        user = req.user
        if check_password(current_password,user.password):
            new_password = req.POST.get("password1")
            password_confirm = req.POST.get("password2")
            if new_password == password_confirm and len(new_password)>8:
                user_name.name = req.POST.get("name")
                user_name.save()
                user.set_password(new_password)
                user.save()
                auth.login(req,user)
                messages.info(req,"정보가 변경 되었습니다.")
                return redirect('home:index')
            elif len(new_password)==0 and len(password_confirm)==0:
                user_name.name = req.POST.get("name")
                user_name.save()
                messages.info(req, "정보가 변경 되었습니다.")
                return redirect('home:index')
            else:
                messages.info(req,"새로운 비밀번호를 확인해 주세요.")
        else:
            messages.info(req,"기존 비밀번호가 일치하지 않습니다.")

    return redirect("home:mypage")

def dismember(req):

    user_name = Profile.objects.get(user=auth.get_user(req))
    context= {'user_name':user_name}

    if req.method == "POST":
        current_password = req.POST.get("password")
        user = req.user
        if check_password(current_password,user.password):
                auth.logout(req)
                user.delete()
                messages.info(req,'탈퇴 처리 되었습니다.')
                return redirect('home:index')
        else:
            messages.info(req,'비밀번호가 일치하지 않습니다.')

    return render(req, "mypage.html",context)

@csrf_exempt
def search_record(req):
    date1 = req.POST['date1']
    date2 = req.POST['date2']

    # section = UserLog.objects.get(pk=1)
    # section_items = TV4SectionItem.objects.values().filter(section=section).prefetch_related('content_object').order_by(
    #     'item_order')
    # ret['section_items'] = list(section_items)

    # context["questions"] = UserLog.objects.prefetch_related('choices')

    testuobj = serializers.serialize('json',UserLog.objects.all())
    return JsonResponse(testuobj,safe=False)

    # context={'date1':date1, 'date2':date2, 'testuobj':testuobj}
    # return HttpResponse(json.dumps(context), content_type="application/json")


