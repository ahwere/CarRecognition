from django import forms
from home.models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name',)