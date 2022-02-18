from dataclasses import field
from xml.dom.minidom import Attr
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from mails.models import *


class adduser(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter your Password'}))

    class Meta:
        model = users
        fields = '__all__'

        # widgets = {
        #     'name': forms.CharField(attrs={'placeholder': 'Name'}),
        #     'employee_id': forms.CharField(
        #         attrs={'placeholder': 'Enter description here'}),
        #     'email_id': forms.CharField(attrs={'placeholder': 'Enter description here'})
        # }
