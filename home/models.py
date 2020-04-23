from django.db import models
from recognition.models import Cctv
from django.contrib.auth.models import User
# Create your models here.

class UserLog(models.Model) :
    user = models.ForeignKey('auth.User', to_field='username', on_delete=models.CASCADE)
    search_time = models.DateTimeField()
    cctv_id = models.ForeignKey(Cctv, to_field='id', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = "UserLog"