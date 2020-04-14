from django.db import models
# Create your models here.

class CctvLog(models.Model) :
    username = models.ForeignKey('auth.User', to_field='username', on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    time = models.DateTimeField()
    color = models.CharField(max_length=20)
    direction = models.TextChoices('front', 'back')
