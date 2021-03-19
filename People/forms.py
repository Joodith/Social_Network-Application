from django import forms
from People.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

import re

class UserRegisterForm(UserCreationForm):
    #password1=forms.CharField(widget=forms.PasswordInput,help_text=None)
    class Meta:
        model=User
        fields=('username','password1')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password1'].label="Password"
        self.fields['username'].help_text=None
        self.fields['password1'].help_text = None



class UserLoginForm(forms.Form):
    username = forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)

class UserExtraDetailsForm(forms.ModelForm):


    class Meta:
        model=Profile
        fields=('full_name',)





class VerifyCodeForm(forms.Form):
    otp=forms.IntegerField()


class BirthdayForm(forms.ModelForm):
    bday=forms.DateField()
    class Meta:
        model=Profile
        fields=('bday',)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('bio','profile_pic')


