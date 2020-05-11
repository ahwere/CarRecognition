from django.db import models
from car.models import Car
# Create your models here.

class Cctv(models.Model) :
    video_link = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    latitude = models.CharField(max_length=20, default='')
    longtitude = models.CharField(max_length=20, default='')

    class Meta:
        db_table = "Cctv"

class CctvLog(models.Model) :
    car_model = models.ForeignKey(Car, to_field='model', on_delete=models.CASCADE, default='')
    color = models.CharField(max_length=20)
    appearance_time = models.DateTimeField()
    direction = models.TextChoices('front', 'back')
    cctv_id = models.ForeignKey(Cctv, to_field='id', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = "CctvLog"