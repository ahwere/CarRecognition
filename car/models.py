from django.db import models
# Create your models here.

class Car(models.Model) :
    model = models.CharField(unique=True, max_length=20)
    brand = models.CharField(max_length=20)
    type = models.CharField(max_length=20)