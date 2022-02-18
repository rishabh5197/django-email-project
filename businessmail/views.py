from time import sleep
# import cv2
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib.auth.models import *
from django.core.mail import send_mail, EmailMultiAlternatives
# EmailMultiAlternatives = for django html mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Q
import os


# def login(request):
#     print('this is in bussiness')
#     return render(request,'mails/login.html')