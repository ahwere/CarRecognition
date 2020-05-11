from django.db import models
from recognition.models import Cctv
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model) :
    class MemberPermission(models.TextChoices):
        ADMIN = 'admin'
        MEMBER = 'member'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    permission = models.CharField(MemberPermission.choices, default=MemberPermission.MEMBER, max_length=10)

    class Meta:
        db_table = 'Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class UserLog(models.Model) :
    user = models.ForeignKey('auth.User', to_field='username', on_delete=models.CASCADE)
    search_time = models.DateTimeField()
    end_time = models.DateTimeField()
    cctv_id = models.ForeignKey(Cctv, to_field='id', on_delete=models.CASCADE, default='')

    class Meta:
        db_table = "UserLog"