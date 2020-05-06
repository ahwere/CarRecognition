from django.shortcuts import render,redirect
from home.models import Profile
from django.contrib import auth
from django.contrib import messages

from car.models import Car
from django.db.models import Count, Q
# Create your views here.
def statistic(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user_name = Profile.objects.get(user=auth.get_user(req))

        return render(req, "statistic_Service.html",{'user_name':user_name})
    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')

def stat(req):
    cur_user = req.user

    if cur_user.is_authenticated:
        user_name = Profile.objects.get(user=auth.get_user(req))

        cctv = req.POST['cctv']
        context = {
            'cctv': cctv,
            'user_name': user_name
        }
        return render(req, "statistic_Service.html", context)

    else:
        messages.info(req, '로그인 후 이용가능합니다.')
        return redirect('home:index')


# #############################################################
def test(req):
    # dataset = Car.objects \
    #     .values('brand') \
    #     .annotate(kia_count=Count('brand', filter=Q(brand=True)),
    #               hyundai_count=Count('brand', filter=Q(brand=False))) \
    #     .order_by('brand')

    dataset = Car.objects.values('model').annotate(something=Count('model'))
    # hello = Car.objects.values('model').annotate(nothing=Count('model'))

    return render(req, 'test.html', {'dataset': dataset})

# def ticket_class_view(request):
#     dataset = Passenger.objects \
#         .values('ticket_class') \
#         .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
#                   not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
#         .order_by('ticket_class')
#     return render(request, 'ticket_class.html', {'dataset': dataset})