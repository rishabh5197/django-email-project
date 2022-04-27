from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from multiprocessing import context
from time import sleep
from email import encoders
import time
from urllib.request import Request
from django.core.mail import send_mail
from os.path import basename
# import cv2
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import datetime
from .models import *
from django.contrib.auth.models import *
from django.core.mail import send_mail, EmailMultiAlternatives
# EmailMultiAlternatives = for django html mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import Settings, settings
from django.db.models import Q
import os
from email.mime.image import MIMEImage
from email.mime import text
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
from django.core.paginator import Paginator
from .forms import *
from mails.models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime
from businessmail.settings import MEDIA_URL
from django.http import FileResponse
from .task import *
import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from email.mime.application import MIMEApplication
import random
# from captcha.image import ImageCaptcha
from .captcha import *

minimum_seconds = -1
maximum_seconds = 30*60
# enter in minutes * 60
# or
# enter directly in seconds


# Login function if for the user to
# login into his own account and proceed for OTP.


def editprofile(request):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        print(request.session.get('email_address'))
        fetching_old_details = users.objects.filter(
            email_id=request.session.get('email_address'))
        print(fetching_old_details)
        if request.method == 'POST':
            print(request.method)
            name = request.POST.get('nameofperson')
            mobile_number = request.POST.get('mobilenumberofperson')
            address = request.POST.get('addressofperson')
            users.objects.filter(email_id=request.session.get(
                'email_address')).update(name=name,
                                         mobile_number=mobile_number,
                                         address=address)
            return render(request, "mails/editprofilepage.html", {'userdetails': fetching_old_details, 'username': request.session.get('name'), 'msg': 'Your profile has been updated successully...'})
        return render(request, 'mails/editprofilepage.html', {'userdetails': fetching_old_details, 'username': request.session.get('name')})
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def creategroup(request):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        print(request.session.get('email_address'))
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        print(db)
        all_members = mail_members.objects.all()
        if request.method == 'POST':
            group_name = request.POST.get('groupname')
            checking_group_name = groups.objects.filter(group_name=group_name)
            if checking_group_name:
                return render(request, 'mails/creategroup.html', {'db': db, 'all_members': all_members, 'errmsg': f'{group_name} already exists'})
            else:
                checked = request.POST.getlist('check')
                print(group_name, checked)
                aa = groups.objects.create(group_name=group_name)
                aa.save()
                for i in checked:
                    bb = group_members.objects.create(email_address=i,
                                                      group_name=group_name)
                    bb.save()
                print('all inserted...')
            return render(request, 'mails/creategroup.html', {'db': db, 'all_members': all_members, 'msg': 'Group Created Successfully...'})

        else:
            return render(request, 'mails/creategroup.html', {'db': db,
                                                              'all_members': all_members
                                                              })
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def addgroupmember(request, group_name):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        all_members = [x['email_address'] for x in list(
            mail_members.objects.all().values('email_address'))]
        present_users = [x['email_address'] for x in list(group_members.objects.filter(
            group_name=group_name).values('email_address'))]
        users_to_be_added = []
        for i in all_members:
            if i in present_users:
                pass
            else:
                users_to_be_added.append(i)
        if request.method == 'POST':
            checked = request.POST.getlist('check')
            print(group_name, checked)
            for i in checked:
                bb = group_members.objects.create(email_address=i,
                                                  group_name=group_name)
                bb.save()
            return redirect(f'/editgroupdetails/{group_name}')

        else:
            return render(request, 'mails/addtoexistinggroup.html', {'db': db, 'group_name': group_name,
                                                                     'users_to_be_added': users_to_be_added})
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def deletegroupmembers(request, email_address, group_name):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        group_members.objects.filter(
            email_address=email_address, group_name=group_name).delete()
        data_rendering = []
        all_group_members = group_members.objects.filter(
            group_name=group_name).values('email_address')
        for i in all_group_members:
            data_mail_members = mail_members.objects.filter(
                email_address=i['email_address']).values_list('name', 'phone_number', 'industry_name')
            print(data_mail_members)
            data_rendering.append(
                [i['email_address'], data_mail_members[0][0], data_mail_members[0][1], data_mail_members[0][2]])
        return render(request, 'mails/editgroupdetails.html', {'db': db, 'group_name': group_name,
                                                               'data_rendering': data_rendering})

    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def viewgroups1(request):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')

    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        all_groups = groups.objects.all()
        print(all_groups)
        return render(request, 'mails/viewgroups2.html', {'db': db,
                                                          'all_groups': all_groups
                                                          })
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def viewgroupdetails1(request, group_name):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        data_rendering = []
        all_group_members = group_members.objects.filter(
            group_name=group_name).values('email_address')
        for i in all_group_members:
            data_mail_members = mail_members.objects.filter(
                email_address=i['email_address']).values_list('name', 'phone_number', 'industry_name')
            print(data_mail_members)
            data_rendering.append(
                [i['email_address'], data_mail_members[0][0], data_mail_members[0][1], data_mail_members[0][2]])
            print('----------------------------------')
        # print(data_rendering)
        return render(request, 'mails/viewgroupdetails2.html', {'db': db, 'group_name': group_name,
                                                                'data_rendering': data_rendering})
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def editgroupdetails(request, group_name):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        data_rendering = []
        all_group_members = group_members.objects.filter(
            group_name=group_name).values('email_address')
        for i in all_group_members:
            data_mail_members = mail_members.objects.filter(
                email_address=i['email_address']).values_list('name', 'phone_number', 'industry_name')
            print(data_mail_members)
            data_rendering.append(
                [i['email_address'], data_mail_members[0][0], data_mail_members[0][1], data_mail_members[0][2]])
        return render(request, 'mails/editgroupdetails.html', {'db': db, 'group_name': group_name,
                                                               'data_rendering': data_rendering})
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


def login(request):
    try:
        msg = request.session.get('msg')
        del request.session['msg']
    except Exception as e:
        msg = None
    print('coming to login')
    if request.method == 'POST':
        email_id = request.POST['email']
        check_exist = users.objects.filter(email_id=email_id)
        oncreationexist = users.objects.filter(
            email_id=email_id).values('on_creation_password')
        print('Yes on creation password exists.....', oncreationexist)
        if check_exist:
            password = request.POST['password']
            user_data = users.objects.filter(email_id=email_id)
            print(list(user_data.values_list()[0]))
            password_verification = pbkdf2_sha256.verify(
                password, user_data.values_list()[0][4])
            # print(user_data.values_list()[0])
            # making status inactive....
            if user_data.values_list()[0][13] >= 3:
                get_data = users.objects.filter(
                    email_id=email_id).update(status=False)
                # print('making inactive', get_data)
            else:
                pass
            if password_verification:
                if int(user_data.values_list()[0][13]) < 3:
                    request.session['name'] = user_data.values_list()[0][1]
                    request.session['email_address'] = request.POST['email']
                    if 'OTPbutton' in request.POST:
                        otp = request.POST['OTP']
                        print(otp)
                        filtering_value = users.objects.filter(
                            email_id=email_id, otp=otp)
                        print('----------------------------------------',
                              filtering_value)
                        if len(filtering_value) > 0 and len(filtering_value) < 2:
                            print("came in if condition......")
                            request.session['approval'] = 'yes'
                            request.session['verified'] = 'yes'
                            users.objects.filter(
                                email_id=email_id).update(attempts=0)
                            return redirect('/selection')
                        else:
                            return render(request, 'mails/login.html', {'errmsg': 'OTP not validated...'})
                    else:
                        sending_otp = random.randrange(10000000, 99999999)
                        users.objects.filter(
                            email_id=email_id).update(otp=sending_otp)
                        send_mail('Login OTP verification ',
                                  f'The otp to verify the account is {sending_otp}',
                                  settings.EMAIL_HOST_USER,
                                  [request.session.get('email_address')],
                                  fail_silently=False,)
                        return render(request, 'mails/login.html', {'enterotp': True, 'email_id': email_id, 'password': password})
                else:
                    return render(request, 'mails/login.html', {'errmsg': 'Cannot login, account locked, please contact admin ', 'msg': msg})
            else:
                if user_data.values_list()[0][3]:
                    attempt_left = 2-user_data.values_list()[0][13]
                    if attempt_left > 0:
                        errmsg = f'Be careful you have {attempt_left} left '
                    else:
                        errmsg = 'You have no attempt left'
                    no_of_attempts = int(user_data.values_list()[0][13])+1
                    users.objects.filter(email_id=email_id).update(
                        attempts=no_of_attempts,
                    )
                    return render(request, 'mails/login.html', {'errmsg': errmsg, 'msg': msg})
                else:
                    return render(request, 'administrative/login.html', {'msg': 'Cannot logged in. Invalid Credentials', 'msg': msg})
        # return render(request, 'administrative/login.html,'msg':msg')
        else:
            return render(request, 'mails/login.html', context={'errmsg': "Email Address does not exist"})
    return render(request, 'mails/login.html', context={'errmsg': msg})


def validatewithotp(request):
    if request.session.get('email_address'):
        if users.objects.filter(email_id=request.session.get(
                'email_address')).values('approval')[0]['approval'] == True:
            request.session['approval'] = 'yes'
            otp_database = users.objects.filter(
                email_id=request.session.get('email_address')).values('otp')
            otp_created = otp_database[0]['otp']
            if request.method == 'POST':
                email_address = request.POST.get('otp_entered')
                if otp_database[0]['otp'] == email_address:
                    users.objects.filter(
                        email_id=request.session.get('email_address')).update(otp=None, attempts=0)
                    request.session['verified'] = 'yes'
                    return redirect('/selection')
                else:
                    request.session['msg'] = 'Invalid OTP or entered wrong OTP.'
                    return redirect('/')
            else:
                send_mail('Login OTP verification ',
                          f'The otp to verify the account is {otp_created}',
                          settings.EMAIL_HOST_USER,
                          [request.session.get('email_address')],
                          fail_silently=False,)
            return render(request, 'mails/validatewithotp.html', {})
        else:
            request.session['msg'] = 'Requested admin to approve your email Address'
            return redirect('/')
            # return render(request,'mails/login.html',{'errmsg':'Requested admin to approve your email Address'})
    else:
        return redirect('/')


def dashboard(request):
    a = request.session.get('name')
    if a:
        return render(request, 'mails/dashboard.html', {
            'name': request.session['name'],
        })
        # else:
    else:
        return redirect('/')


# This is for selection of items that are present on the homescreen.
# A user will be able to select the items...
def selection(request):
    if request.session.get('time'):
        request.session.get('time')
        print('time already present')
        print(request.session.get('time'), 'current time....')
    else:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(new_time)
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')

    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        print(request.session.get('email_address'))
        db = users.objects.filter(
            email_id=request.session.get('email_address'))
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        return render(request, 'mails/homepage.html', {'user': request.session.get('name'), 'db': db})
    else:
        print('coming to else')
        if request.session.get('time'):
            del request.session['time']
            try:
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
                request.session['msg'] = 'Logged out due to inactive state'
                print('deleted session', request.session.get('time'))
            except:
                pass

        else:
            print('coming to nested else')
            pass

        return redirect('/')


# Database of all emails.
# here is the list of all emails.
def storedmails(request):
    try:
        new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
        print(request.session.get('time'))
        difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                      datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
        print(str(difference) + ' seconds')
    except:
        pass
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        all_emails = mails.objects.all()
        return render(request, 'mails/databasemails.html', {'mails': all_emails, 'count': 0})
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# user will send email with from to etc.
def sendemail(request, title=''):
    # print(request.method)
    group = groups.objects.all()
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        all_mail_members = list(
            mail_members.objects.all().values('email_address'))
        print(all_mail_members)
        json_data = json.dumps(all_mail_members)
        form = sentmails()
        if title:
            # print(title)
            fetched_details = list(mails.objects.filter(
                title=title).values_list('title', 'describe', 'attachments'))
            print(fetched_details)
            form = sentmails(initial={'describe': fetched_details[0][1]})
            return render(request, 'mails/sendemail.html', {'title': fetched_details[0][0],
                                                            'attachments': fetched_details[0][2], 'form': form, 'json_data': json_data, 'groups': group})
            print(fetched_details[0][2])

        if request.method == "POST":
            checks = request.POST.getlist('check')
            to = list(request.POST.get("to").split(","))
            for i in checks:
                mail_to_group = [x[0] for x in group_members.objects.filter(
                    group_name=i).values_list('email_address')]
                print('adding all', i, 'to the list...')
                to.extend(mail_to_group)
            print(to)
            cc = list(request.POST.get("cc").split(","))
            bcc = list(request.POST.get("bcc").split(","))
            title = request.POST.get("title")
            description = request.POST.get("describe")
            attachments = request.FILES.get("document")
            allowed_items = ['docx', 'jpg', 'png',
                             'pdf', 'bmp', 'ico', 'gif', 'jpeg']
            # attachments_type = request.POST.get("document").split(".")[-1]
            # print(attachments_type)
            # form = MailForm(request.POST)
            # print('Checking if the form is valid or not... ',form.is_valid())
            # if form.is_valid():
            #     form.save()

            print(attachments,
                  '-------------------------------------------------------------------------')
            # person_resume = request.FILES.get('resume')
            if attachments:
                print("yes there is attachments...............")
            else:
                print("awww failed to take it.....")
            print(to, title, description, attachments)
            try:
                mails.objects.create(title=title,
                                     describe=description,
                                     attachments=attachments,
                                     extension=((attachments.name).split(".")[-1]).lower())
            except Exception as e:
                mails.objects.create(title=title,
                                     describe=description,
                                     attachments=attachments)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d %B, %Y")
            sent_mails.objects.create(by=request.session.get('email_address'),
                                      to=to,
                                      cc=cc,
                                      bcc=bcc,
                                      subject=title,
                                      describe=description,
                                      attachments=attachments,
                                      time=current_time,
                                      date=current_date,
                                      status=False)
            email = EmailMultiAlternatives(
                # subject,content,from,to people(list)
                title,
                description,
                settings.EMAIL_HOST_USER,
                to=to,
                cc=cc,
                bcc=bcc
            )
            # print(((attachments.name).split(".")[-1]).lower())
            if attachments:
                if (((attachments.name).split(".")[-1]).lower() in allowed_items):
                    # try:
                    if ((attachments.name).split(".")[-1]).lower() in ['jpg', 'png', 'bmp', 'ico', 'gif', 'jpeg']:
                        # email = EmailMultiAlternatives(
                        #     # subject,content,from,to people(list)
                        #     title,
                        #     description,
                        #     settings.EMAIL_HOST_USER,
                        #     to=to,
                        #     cc=cc,
                        #     bcc=bcc
                        # )
                        mime_image = MIMEImage(attachments.read())
                        mime_image.add_header(
                            'Content-Disposition', "attachment; filename= %s" % attachments)
                        email.attach(mime_image)
                        email.attach_alternative(description, "text/html")
                        email.send()
                        # mime_image = MIMEImage(attachments.read())
                    # except Exception as e:
                    else:
                        print("checking for documents....")

                        # message = send_mail(title, description,  settings.EMAIL_HOST_USER, to, html_message=description)
                        # # message.attach('Attachment.pdf', attachments, 'file/pdf')
                        # message.attach_file(attachments)
                        # message.send()
                        # pdf = render_to_pdf(attachments)

                        # email.attach(attachments.name, attachments.read(),attachments.content_type)
                        # email.send()

                        # mail = MIMEBase(attachments.read(), _subtype=((attachments.name).split(".")[-1]).lower())
                        # email.attach(mail)
                        # email.attach_alternative(description, "text/html")
                        # attachment = MIME(attachments.read())
                        # attachment.add_header('Content-Disposition', "attachment; filename= %s" % attachments)
                        # email.attach(attachment)
                        # email.attach_alternative(description, "text/html")
                        # email.send()

                        # print(f"""'{((attachments.name).split(".")[-1]).lower()}'""")
                        # file = MIMEApplication(attachments.read(), _subtype=((attachments.name).split(".")[-1]).lower())
                        # email.attach(file)
                        # email.attach(attachments.name, attachments.read(), f"""'{((attachments.name).split(".")[-1]).lower()}'""")

                        # email.attach(attachments.name, attachments.read(), ((attachments.name).split(".")[-1]).lower())
                        # filename = attachments
                        # see for location if error occurs
                        # attachment = open(attachments, "rb")
                        # part = MIMEBase('application', 'octet-stream')
                        # part.set_payload(attachments.read())
                        # encoders.encode_base64(part)
                        # part.add_header('Content-Disposition',"attachment; filename= %s" % attachments)

                        # # Attach the attachment to the MIMEMultipart object
                        # msg.attach(part)
                        # email.attach(part)

                        # ------------------------------------------------------------------------------------------------------
                        # email = EmailMessage(title, description, settings.EMAIL_HOST_USER, to=to,cc=cc,bcc=bcc)
                        # email.attach_file(attachments)
                        # email.send()

                        #  -----------------------------------------------------------------------------------------------------
                        # part = MIMEApplication(attachments.read(),((attachments.name).split(".")[-1]).lower())
                        # part.add_header('Content-Disposition',"attachement; filename="+(attachments.name))
                        # email.attach(part)
                        # email.attach_alternative(description, "text/html")
                        # email.send()

                        # -----------------------------------------------------------------------------------------------------
                        # part = MIMEApplication(attachments.read(),Name=basename(attachments))
                        # # After the file is closed
                        # part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachments)
                        # email.attach(part)

                else:
                    return render(request, 'mails/sendemail.html', {'msg': 'not a valid type of file, file must be .jpg,.png,.pdf,.bmp,.ico,.gif or .jpeg,', 'form': form, 'json_data': json_data, 'groups': group})
            email.attach_alternative(description, "text/html")
            email.send()
            sent_mails.objects.filter(by=request.session.get('email_address'),
                                      subject=title,
                                      time=current_time,
                                      date=current_date).update(status=True)
            return render(request, 'mails/sendemail.html', {'msg': "Email sent successfully.", 'form': form, 'json_data': json_data})

        return render(request, 'mails/sendemail.html',
                      {'form': form, 'json_data': json_data, 'groups': group})
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# for logging out from the webpage
def signout(request):
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes':
        del request.session['time']
        del request.session['name']
        del request.session['verified']
        del request.session['email_address']
        return redirect('/')
    else:
        if request.session.get('time'):
            del request.session['time']
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# to see all email ids.
def viewemailids(request):
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        all_members = mail_members.objects.all()
        return render(request, 'mails/viewemailids.html', {'emails': all_members})
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# this is for scheduling mails.
def schedulemail(request, title=''):
    form = sentmails()
    group = groups.objects.all()
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        if title:
            # print(title)
            fetched_details = list(mails.objects.filter(
                title=title).values_list('title', 'describe', 'attachments'))
            form = sentmails(initial={'describe': fetched_details[0][1]})
            # for i in os.listdir(settings.MEDIA_ROOT):
            #     for j in os.listdir(settings.MEDIA_ROOT+'/'+i):
            #         os.open()

            path_to_file = settings.MEDIA_ROOT.replace(
                '\\', '/')+'/'+fetched_details[0][2]
            # os.open(path_to_file,'rb')
            # FileResponse(open(path_to_file, 'rb'))
            # file_to_be_downloaded = settings.MEDIA_ROOT + fetched_details[0][2]
            # file_to_be_downloaded.
            return render(request, 'mails/schedulemail.html', {'groups': group, 'title': fetched_details[0][0],
                                                               'attachments': path_to_file, 'form': form, })
        if request.method == 'POST':
            checks = request.POST.getlist('check')
            to = list(request.POST.get("to").split(","))
            for i in checks:
                mail_to_group = [x[0] for x in group_members.objects.filter(
                    group_name=i).values_list('email_address')]
                print('adding all', i, 'to the list...')
                to.extend(mail_to_group)
            print(to)
            cc = list(request.POST.get("cc").split(","))
            bcc = list(request.POST.get("bcc").split(","))
            title = request.POST.get('title')
            description = request.POST.get("describe")
            attachment = request.FILES.get('document')
            date = request.POST.get('date')
            time = request.POST.get('time')
            user_action = request.POST.get('get_time_action')
            print(
                '++++++++++++++++-----------------+++++++++++++++++++++---------------', user_action)
            session_user = request.session.get('email_address')
            start_date = request.POST.get('dailystartdate')
            end_date = request.POST.get('dailyenddate')
            startweek = request.POST.get('startweek')
            endweek = request.POST.get('endweek')
            startmonth = request.POST.get('startmonth')
            endmonth = request.POST.get('endmonth')
            weekday = request.POST.get('weekday')
            dateofmonth = request.POST.get('dateofmonth')
            print('-----------------------------------------------------',
                  start_date, 'and', end_date)
            print('-----------------------------------------------------',
                  startweek, 'and', endweek)
            print('-----------------------------------------------------',
                  startmonth, 'and', endmonth)
            if user_action == 'specific_time':
                # splitting hour and minutes...
                hour, minute = time.split(':')[0], time.split(':')[1]
                print(to, cc, bcc, title, attachment, description, date, time)

                # Splitting days and month from user input
                year, month, day = date.split(
                    '-')[0], date.split('-')[1], date.split('-')[2]
                # print('this is date splitted :-',year,'/',month,'/',day)

                # Here starts scheduling-----------------------------------------------------
                schedule, created = CrontabSchedule.objects.get_or_create(
                    hour=hour, minute=minute, day_of_month=month, month_of_year=day)

                # schedulemail.delay(to,cc,bcc,title,description,attachment)

                task = PeriodicTask.objects.create(
                    crontab=schedule, name=title+" "+date+" "+time, task='mails.task.schedulemail')

                # Here ends scheduling-----------------------------------------------------
                adding_to_schedule = schedulemails.objects.create(by=settings.EMAIL_HOST_USER,
                                                                  to=to,
                                                                  cc=cc,
                                                                  bcc=bcc,
                                                                  subject=title,
                                                                  describe=description,
                                                                  attachments=attachment,
                                                                  date=date,
                                                                  time=time,
                                                                  session_user=session_user
                                                                  )
                adding_to_schedule.save()
                print(request.session.get('email_address'))
                print('storing to database successful....')
                print(
                    '**********************************************************************Task schedule successfully....')
                return render(request, 'mails/schedulemail.html', {'msg': 'Email Schedule Successfully.....', 'form': form, 'groups': group})
            elif user_action == 'daily':
                print(start_date, end_date)
                user_start_month, user_start_date = start_date.split(
                    '-')[1], start_date.split('-')[2]
                user_end_month, user_end_date = end_date.split(
                    '-')[1], end_date.split('-')[2]
                print(user_start_date+"-"+user_end_month,
                      user_start_month+"-"+user_end_date)
                # the time is set to 8:00 AM Mauritian time.
                if user_start_month == user_end_month:
                    schedule, created = CrontabSchedule.objects.get_or_create(
                        hour='*', minute='*', month_of_year=f"{user_start_month}")
                else:
                    schedule, created = CrontabSchedule.objects.get_or_create(
                        hour='8', minute='30', month_of_year=f"{user_start_month}-{user_end_month}")
                # # schedulemail.delay(to,cc,bcc,title,description,attachment)
                task = PeriodicTask.objects.create(
                    crontab=schedule, name=title+" "+start_date+" "+end_date, task='mails.task.dailymails')
                adding_to_daily_schedule = dailymailsdatabase.objects.create(by=settings.EMAIL_HOST_USER,
                                                                             to=to,
                                                                             cc=cc,
                                                                             bcc=bcc,
                                                                             subject=title,
                                                                             describe=description,
                                                                             attachments=attachment,
                                                                             session_user=session_user,
                                                                             start_date=start_date,
                                                                             end_date=end_date,
                                                                             status=True)
                adding_to_daily_schedule.save()
                return render(request, 'mails/schedulemail.html', {'msg': 'Email Schedule Successfully.....', 'form': form, 'groups': group})
            elif user_action == 'weekly':
                print(startweek, endweek, weekday)
                print(startweek.split('-'))
                print(endweek.split('-'))
                user_start_month, user_start_date = startweek.split(
                    '-')[1], startweek.split('-')[2]
                user_end_month, user_end_date = endweek.split(
                    '-')[1], endweek.split('-')[2]
                print(user_start_date+"-"+user_end_month,
                      user_start_month+"-"+user_end_date)
                # the time is set to 8:00 AM Mauritian time.
                if user_start_month == user_end_month:
                    schedule, created = CrontabSchedule.objects.get_or_create(
                        hour='*', minute='*', day_of_week=weekday)
                else:
                    schedule, created = CrontabSchedule.objects.get_or_create(
                        hour=8, minute=00, month_of_year=f"{user_start_month}-{user_end_month}", day_of_week=weekday)
                # # schedulemail.delay(to,cc,bcc,title,description,attachment)
                task = PeriodicTask.objects.create(
                    crontab=schedule, name=title+" "+start_date+" "+end_date, task='mails.task.weekmails')
                adding_to_weekly_schedule = weeklymailsdatabase.objects.create(by=settings.EMAIL_HOST_USER,
                                                                               to=to,
                                                                               cc=cc,
                                                                               bcc=bcc,
                                                                               subject=title,
                                                                               describe=description,
                                                                               attachments=attachment,
                                                                               session_user=session_user,
                                                                               start_date=startweek,
                                                                               end_date=endweek,
                                                                               day=weekday,
                                                                               status=False)
                adding_to_weekly_schedule.save()
                return render(request, 'mails/schedulemail.html', {'msg': 'Email Schedule Successfully.....', 'form': form, 'groups': group})
            elif user_action == 'monthly':
                print(startmonth, endmonth, dateofmonth)
                if startmonth == endmonth:
                    schedule, created = CrontabSchedule.objects.get_or_create(
                        hour='*', minute='*', month_of_year=f'{startmonth}', day_of_month=dateofmonth)
                else:
                    schedule, created = CrontabSchedule.objects.get_or_create(
                        hour='9', minute='30', month_of_year=f'{startmonth}-{endmonth}', day_of_month=dateofmonth)
                adding_to_monthly_schedule = monthlymailsdatabase.objects.create(by=settings.EMAIL_HOST_USER,
                                                                                 to=to,
                                                                                 cc=cc,
                                                                                 bcc=bcc,
                                                                                 subject=title,
                                                                                 describe=description,
                                                                                 attachments=attachment,
                                                                                 session_user=session_user,
                                                                                 startmonth=startmonth,
                                                                                 endmonth=endmonth,
                                                                                 dayofmonth=dateofmonth,
                                                                                 status=False)
                adding_to_monthly_schedule.save()
                print('added to monthly schedule....')
                return render(request, 'mails/schedulemail.html', {'msg': 'Email Schedule Successfully.....', 'form': form, 'groups': group})
            else:
                return render(request, 'mails/schedulemail.html', {'msg': 'Invalid Selection...', 'form': form, 'groups': group})

        return render(request, 'mails/schedulemail.html', {'form': form, 'groups': group})
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# to see all the groups present in the application
def viewgroups(request):
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        all_groups = groups.objects.all()
        print(all_groups)
        return render(request, 'mails/viewgroups.html', {
            'all_groups': all_groups
        })
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# to view details of all groups.
def viewgroupdetails(request, group_name):
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > minimum_seconds and difference < maximum_seconds:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        data_rendering = []
        all_group_members = group_members.objects.filter(
            group_name=group_name).values('email_address')
        for i in all_group_members:
            data_mail_members = mail_members.objects.filter(
                email_address=i['email_address']).values_list('name', 'phone_number', 'industry_name')
            print(data_mail_members)
            data_rendering.append(
                [i['email_address'], data_mail_members[0][0], data_mail_members[0][1], data_mail_members[0][2]])
            print('----------------------------------')
        # print(data_rendering)
        return render(request, 'mails/viewgroupdetails.html', {'group_name': group_name,
                                                               'data_rendering': data_rendering})
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')


# list of sent emails.
def sentmailslist(request):
    new_time = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
    print(request.session.get('time'))
    difference = (datetime.strptime(new_time, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')).seconds
    print(str(difference) + ' seconds')
    if request.session.get('name') and request.session.get('verified') == 'yes' and request.session.get('approval') == 'yes' and difference > -1 and difference < 1800:
        request.session['time'] = datetime.strftime(
            datetime.now(), '%d/%m/%Y %H:%M:%S')
        mails = request.session['email_address']
        print(mails)
        # mails = sent_mails.objects.filter(
        #     by=mails).order_by('-time').order_by('-date')
        mails = sent_mails.objects.filter(by=mails).order_by('-id')
        return render(request, 'mails/mailsview.html', {'employee_id': request.session.get('email_address'), 'mails': mails})
    else:
        if request.session.get('time'):
            try:
                del request.session['time']
                if request.session['name']:
                    del request.session['name']
                if request.session['verified']:
                    del request.session['verified']
                if request.session['email_address']:
                    del request.session['email_address']
            except:
                pass
            request.session['msg'] = 'Logged out due to inactive state'
        else:
            pass
        return redirect('/')

# create by rishabh at 2:30 14th Feb 2022.
# this is for registering user itself no admin headache.


# def registeruser(request):

#     return render(request, 'mails/registeruser.html', {})


def registeruser(request):
    # image = ImageCaptcha(width=280, height=90)
    # captcha_code = str(random.randrange(10000000,99999999))
    # print(captcha_code)
    # data = image.generate(captcha_code)
    # image.write(captcha_code, 'CAPTCHA.png')
    captcha_code = FormWithCaptcha
    if request.method == "POST":
        name = request.POST['name']
        # employee_id = request.POST['employee_id']
        # department = request.POST['department']
        email_id = request.POST['email_id']
        mobile_number = request.POST['mobile']
        address = request.POST['address']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        security_question_1 = request.POST['question_1']
        answer_1 = request.POST['answer_1']
        security_question_2 = request.POST['question_2']
        answer_2 = request.POST['answer_2']
        employee_id = "E - "+str(int(users.objects.latest('id').id)+1)
        # captcha_typed = request.POST['captcha_typed']
        if password != confirm_password:
            print("password doesn't match")
            return render(request, 'mails/registeruser.html', {'errmsg': 'Password not matching...', 'captcha_code': captcha_code})
        else:
            print("password match")
            if (security_question_1 == security_question_2):
                print('Both Questions are same.')
                return render(request, 'mails/registeruser.html', {'errmsg': "security questions can't be same", 'captcha_code': captcha_code})
            else:
                # to encrypt
                # -------------- pbkdf2_sha256.encrypt(password, rounds=30000, salt_size=64)
                encrypted_password = pbkdf2_sha256.encrypt(
                    password, rounds=30000, salt_size=32)
                # to verify
                # -------------- pbkdf2_sha256.verify('Newyork@123',encrypted_password)
                # attempts = request.POST['attempts']
                try:
                    print("trying to validate email address")
                    validate_email(email_id)
                    print("email address validated.")
                except ValidationError as e:
                    print("Email - Address Error.")
                    return render(request, 'mails/registeruser.html', {'errmsg': 'Email address invalid', 'captcha_code': captcha_code})
                else:
                    print("good email")
                print(name, email_id, password, mobile_number,
                      address, security_question_1, answer_1, security_question_2, answer_2)
                # exists_check = users.objects.filter(Q(email_id=email_id))
                exists_check = users.objects.filter(email_id=email_id)
                print(exists_check)
                if exists_check:
                    print("there exists email- address")
                    return render(request, 'mails/registeruser.html', {'errmsg': 'Email Id already existing.', 'captcha_code': captcha_code})
                else:
                    otp_created = random.randrange(10000000, 99999999)
                    print(f'otp created...{otp_created}')
                    # session_list=[]
                    # now = datetime.now()
                    # session_list.extend([now.minute])
                    request.session['time'] = datetime.strftime(
                        datetime.now(), '%d/%m/%Y %H:%M:%S')
                    request.session['email_id_to_verify'] = email_id
                    print("Stored to sessions")
                    print("Started creating query")
                    addusertodb = users.objects.create(
                        name=name,
                        employee_id=employee_id,
                        email_id=email_id,
                        password=encrypted_password,
                        mobile_number=mobile_number,
                        # department=department,
                        question_1=security_question_1,
                        question_2=security_question_2,
                        answer_1=answer_1,
                        answer_2=answer_2,
                        address=address,
                        status=False,
                        attempts=0,
                        approval=False,
                        otp=otp_created
                    )
                    addusertodb.save()
                    print("Ended query")
                    print("Trying Email send")
                    send_mail(
                        'OTP verification ',
                        f'The otp to verify the account is {otp_created}',
                        settings.EMAIL_HOST_USER,
                        [email_id],
                        fail_silently=False,
                    )
                    print('mail sent')
                    # return render(request, 'mails/registeruser.html', {'msg': 'User is successfully added to database'})
                    print("redirecting to userverification")
                    return redirect('/userverification')
    else:
        print("there is some failure")
        return render(request, 'mails/registeruser.html', {'captcha_code': captcha_code})


def userverification(request):
    if request.session.get('email_id_to_verify'):
        a = request.session.get('time')
        # a = datetime.strptime(request.session.get('time'), '%d/%m/%Y %H:%M:%S')
        print('This is the time ------------------------------------', a)
        if request.method == 'POST':
            print('--------------------- form is post ---------------------------')
            now = datetime.now()
            now = datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')
            print(datetime.strptime(now, '%d/%m/%Y %H:%M:%S') -
                  datetime.strptime(a, '%d/%m/%Y %H:%M:%S'))
            difference = (datetime.strptime(now, '%d/%m/%Y %H:%M:%S') -
                          datetime.strptime(a, '%d/%m/%Y %H:%M:%S')).seconds
            print(difference)
            if difference < 1200 and difference > -1:
                print(
                    '-------------------------came for otp_entance after getting difference ----------------')
                entered_otp = request.POST.get("otp_entered")
                otp_database = users.objects.filter(
                    email_id=request.session.get('email_id_to_verify')).values('otp')
                print(otp_database[0]['otp'])
                print(entered_otp)
                print(
                    '------------------------------------- got OTP --------------------------------')
                if str(otp_database[0]['otp']) == str(entered_otp):
                    users.objects.filter(email_id=request.session.get(
                        'email_id_to_verify')).update(status=True)
                    print(
                        '------------------------------------- Correct OTP --------------------------------')
                    del request.session['email_id_to_verify']
                    del request.session['time']

                    print(
                        '------------------------------------- Deleted all session --------------------------------')
                    request.session['msg'] = 'id created'
                    # return render(request, 'mails/login.html', {'msg': 'id created and verified successfully'})
                    return redirect('/')
                else:
                    print(
                        '-------------------------returning to login screen but not valid otp----------------')
                    del request.session['email_id_to_verify']
                    del request.session['time']
                    users.objects.filter(email_id=request.session.get(
                        'email_id_to_verify')).delete()
                    print(
                        '------------------------------------- Deleted all session --------------------------------')
                    return render(request, 'mails/login.html', {'errmsg': 'please create id and enter correct OTP again'})
            else:
                print(
                    '-------------------------returning to login screen but Timed out----------------')
                del request.session['email_id_to_verify']
                del request.session['time']
                print(
                    '------------------------------------- Deleted all session --------------------------------')
                users.objects.filter(email_id=request.session.get(
                    'email_id_to_verify')).delete()
                print(
                    '------------------------------------- Deleted from database --------------------------------')
                return render(request, 'mails/login.html', {'msg': 'Timed out you were late please create account again...'})

            # request.session['time'] = time.localtime()
        else:
            print(
                '------------------------ form is GET but not post -----------------------------')
            return render(request, 'mails/otppage.html', {})


def forgetpage(request):
    if request.method == 'POST':
        # if request.POST.get('fetch_id'):
        if 'fetch_id' in request.POST:
            email_address = request.POST.get('email_address')
            print(email_address)
            questions = users.objects.filter(
                email_id=email_address).values_list('question_1', 'question_2')
            question_1, question_2 = questions[0][0], questions[0][1]
            return render(request, 'mails/forgetpage.html', {'email_address': email_address, 'question_1': question_1,
                                                             'question_2': question_2})
        # elif request.POST.get('')
        elif 'validate_answers' in request.POST:
            email_address = request.POST.get('email_address')
            questions = users.objects.filter(
                email_id=email_address).values_list('question_1', 'question_2')
            question_1, question_2 = questions[0][0], questions[0][1]
            answer_1 = request.POST.get('answer_1')
            answer_2 = request.POST.get('answer_2')
            return render(request, 'mails/forgetpage.html', {'email_address': email_address,
                                                             'question_1': question_1,
                                                             'question_2': question_2,
                                                             'answer_1': answer_1,
                                                             'answer_2': answer_2})
    return render(request, 'mails/forgetpage.html', {})

# def groupemail(request, title=''):
#     if request.session.get('name') and request.session.get('verified') == 'yes':
#         group = groups.objects.all()
#         form = sentmails()
#         if title:
#             # print(title)
#             fetched_details = list(mails.objects.filter(
#                 title=title).values_list('title', 'describe', 'attachments'))
#             form = sentmails(initial={'describe': fetched_details[0][1]})
#             # for i in os.listdir(settings.MEDIA_ROOT):
#             #     for j in os.listdir(settings.MEDIA_ROOT+'/'+i):
#             #         os.open()

#             path_to_file = settings.MEDIA_ROOT.replace(
#                 '\\', '/')+'/'+fetched_details[0][2]
#             # os.open(path_to_file,'rb')
#             # FileResponse(open(path_to_file, 'rb'))
#             # file_to_be_downloaded = settings.MEDIA_ROOT + fetched_details[0][2]
#             # file_to_be_downloaded.
#             return render(request, 'mails/groupemail.html', {'groups': group, 'title': fetched_details[0][0],
#                                                              'attachments': path_to_file, 'form': form, })
#         if request.method == 'POST':
#             checks = request.POST.getlist('check')
#             for i in checks:
#                 mail_to_group = [x[0] for x in group_members.objects.filter(
#                     group_name=i).values_list('email_address')]
#                 print(mail_to_group)
#                 to = mail_to_group
#                 title = request.POST.get("title")
#                 description = request.POST.get("describe")
#                 attachments = request.FILES.get("document")
#                 allowed_items = ['docx', 'jpg', 'png',
#                                  'pdf', 'bmp', 'ico', 'gif', 'jpeg']
#                 print('-----------------------------------------------------------')
#                 mails.objects.create(title=title,
#                                      describe=description,
#                                      attachments=attachments)
#                 now = datetime.now()
#                 current_time = now.strftime("%H:%M:%S")
#                 current_date = now.strftime("%d %B, %Y")

#                 sent_mails.objects.create(by=request.session.get('email_address'),
#                                           to=i+' (group)',
#                                           subject=title,
#                                           describe=description,
#                                           attachments=attachments,
#                                           time=current_time,
#                                           date=current_date)
#                 print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#                 email = EmailMultiAlternatives(
#                     # subject,content,from,to people(list)
#                     title,
#                     description,
#                     settings.EMAIL_HOST_USER,
#                     to=to,
#                 )
#                 print(
#                     '------------------------------------------------------- Attaching to email')
#                 # print(((attachments.name).split(".")[-1]).lower())
#                 if attachments:
#                     print(
#                         '---------------------------------------------------- checking attachments')
#                     if (((attachments.name).split(".")[-1]).lower() in allowed_items):
#                         try:
#                             mime_image = MIMEImage(attachments.read())
#                             mime_image.add_header('Content-ID', '<image>')
#                             email.attach(mime_image)
#                         except Exception as e:
#                             print("checking for documents....")
#                             # email.attach(attachments.name,
#                             #              attachments.read(), attachments.content_type)

#                             #  attachment = open('filepath', 'rb')
#                             # msg.attach('Name.txt', attachment.read(), 'text/csv')

#                             attachment = open(attachments, 'rb')
#                             email.attach(attachment,
#                                          attachment.read(), type='text/pdf')
#                     else:
#                         return render(request, 'mails/groupemail.html', {'msg': 'Not a valid type of file, file must be .jpg,.png,.pdf,.bmp,.ico,.gif or .jpeg,', 'form': form})
#             email.send()
#             return render(request, 'mails/groupemail.html', {'form': form, 'groups': group, 'msg': 'email sent to the groups'})
#         return render(request, 'mails/groupemail.html', {'form': form, 'groups': group})
#     else:
#         return redirect('/')
