from dataclasses import field, fields
from django.forms import ModelForm
from .models import *


class mailform(ModelForm):
    class Meta:
        model = mails
        fields = '__all__'


class login(ModelForm):
    class Meta:
        model = users
        fields = '__all__'


class sentmails(ModelForm):
    class Meta:
        model = sent_mails
        fields = '__all__'
