from django.contrib import admin
from recognition.models import Cctv, CctvLog
from home.models import UserLog, Profile
from car.models import Car

# Register your models here.

admin.site.register(Cctv)
admin.site.register(CctvLog)
admin.site.register(UserLog)
admin.site.register(Car)
admin.site.register(Profile)