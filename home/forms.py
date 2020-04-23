from django import forms
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'is_staff', )
        # model = Profile
        # fields = ('user', 'permission',)