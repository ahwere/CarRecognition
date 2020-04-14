from django.db import models
# from django.contrib.auth.models import User
# Create your models here.

class UserLog(models.Model) :
    username = models.ForeignKey('auth.User', to_field='username', on_delete=models.CASCADE)
    search_time = models.DateTimeField()
    search_location = models.CharField(max_length=200)
