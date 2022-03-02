from email.message import EmailMessage
from time import sleep
from urllib import request
# import cv2
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from .models import *
from django.contrib.auth.models import *
from django.core.mail import send_mail, EmailMultiAlternatives
# EmailMultiAlternatives = for django html mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import *
from django.db.models import Q
import os
from email.mime.image import MIMEImage
from email.mime import text
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
from django.core.paginator import Paginator
from .forms import *
from mails.models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import time


def permissions(request, email_address):
    if request.user.is_authenticated:
        db = users.objects.filter(email_id=email_address)
        if request.method == 'POST':
            checked = request.POST.getlist('check')
            print(checked)
            if 'create_group' in checked:
                users.objects.filter(
                    email_id=email_address).update(group_creation=True)
            else:
                users.objects.filter(
                    email_id=email_address).update(group_creation=False)

            if 'modify_group' in checked:
                users.objects.filter(
                    email_id=email_address).update(group_edition=True)
            else:
                users.objects.filter(
                    email_id=email_address).update(group_edition=False)
            return redirect('/administrative/dashboard')
        return render(request, "administrative/permissions.html", {'email_address': email_address,
                                                                   'db': db})
    else:
        return redirect('/administrative/')


def approveuser(request):
    if request.user.is_authenticated:
        full_list = users.objects.filter(approval=False)
        return render(request, 'administrative/approveuser.html', {'users': full_list})
    else:
        return redirect('/administrative/')


def viewgroupdetails(request, group_name):
    if request.user.is_authenticated:
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
        return render(request, 'administrative/viewgroupdetails.html', {'group_name': group_name,
                                                                        'data_rendering': data_rendering})
    else:
        return redirect('/administrative/')


def deletemembers(request):
    if request.user.is_authenticated:
        all_members = mail_members.objects.all()
        return render(request, 'administrative/deletemembers.html', {'all_members': all_members})
    else:
        return redirect('/administrative/')


def deleteemail(request, email_address):
    if request.user.is_authenticated:
        mail_members.objects.filter(email_address=email_address).delete()
        group_members.objects.filter(email_address=email_address).delete()
        return redirect('/administrative/deletemembers')
    else:
        return redirect('/administrative/')


def deletegroupmembers(request, email_address, group_name):
    if request.user.is_authenticated:
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
        return render(request, 'administrative/editgroupdetails.html', {'group_name': group_name,
                                                                        'data_rendering': data_rendering})

    else:
        return redirect('/administrative/')


def addgroupmember(request, group_name):
    if request.user.is_authenticated:
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
            return redirect(f'/administrative/editgroupdetails/{group_name}')

        else:
            return render(request, 'administrative/addtoexistinggroup.html', {'group_name': group_name,
                                                                              'users_to_be_added': users_to_be_added})
    else:
        return redirect('/administrative/')


def editgroupdetails(request, group_name):
    if request.user.is_authenticated:
        data_rendering = []
        all_group_members = group_members.objects.filter(
            group_name=group_name).values('email_address')
        for i in all_group_members:
            data_mail_members = mail_members.objects.filter(
                email_address=i['email_address']).values_list('name', 'phone_number', 'industry_name')
            print(data_mail_members)
            data_rendering.append(
                [i['email_address'], data_mail_members[0][0], data_mail_members[0][1], data_mail_members[0][2]])
        return render(request, 'administrative/editgroupdetails.html', {'group_name': group_name,
                                                                        'data_rendering': data_rendering})
    else:
        return redirect('/administrative/')


def deletegroup(request, group_name):
    if request.user.is_authenticated:
        all = group_members.objects.filter(group_name=group_name)
        return render(request, 'administrative/deletegroup.html', {'group_name': group_name, 'len_of_group': len(list(all))})
    else:
        return redirect('/administrative/')


def confirmdelete(request, group_name):
    if request.user.is_authenticated:
        group_members.objects.filter(group_name=group_name).delete()
        groups.objects.filter(group_name=group_name).delete()
        return redirect('/administrative/viewgroups')
    else:
        return redirect('/administrative/')


def login_admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'administrative/login.html', {'msg': 'cannot logged in. Invalid Credentials'})
    return render(request, 'administrative/login.html')


def viewgroups(request):
    if request.user.is_authenticated:
        all_groups = groups.objects.all()
        print(all_groups)
        return render(request, 'administrative/viewgroups.html', {
            'all_groups': all_groups
        })
    else:
        return redirect('/administrative/')


def user_mails(request, employee_id):
    if request.user.is_authenticated:
        mails = list(users.objects.filter(
            employee_id=employee_id).values('email_id'))[0]['email_id']
        # mails = sent_mails.objects.filter(by=mails).order_by('-date').order_by('-time')
        mails = sent_mails.objects.filter(by=mails).order_by('-id')
        return render(request, 'administrative/mailsview.html', {'employee_id': employee_id, 'mails': mails})
    else:
        return redirect('/administrative/')


def changepassword(request, employee_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            print('method is post')
            password = request.POST['password']
            # to encrypt
            # -------------- pbkdf2_sha256.encrypt(password, rounds=30000, salt_size=64)
            encrypted_password = pbkdf2_sha256.encrypt(
                password, rounds=30000, salt_size=32)
            update_password = users.objects.filter(
                employee_id=employee_id).update(password=encrypted_password)
            print('password is updated...')
            return redirect('/administrative/dashboard')
        else:
            return render(request, 'administrative/changepassword.html', {
                'employee_id': employee_id,
                'form': adduser,
            })
    else:
        return redirect('/administrative/')


def edit(request, employee_id):
    if request.user.is_authenticated:
        user_data = users.objects.filter(employee_id=employee_id)
        email_add_to_use = user_data.values_list()[0][3]
        # print(email_id)
        print('**************************************************************',
              email_add_to_use)
        print(user_data.values_list())
        # print(dict(user_data))
        form = adduser(initial={'name': user_data.values_list()[0][1],
                                'email_id': user_data.values_list()[0][3],
                                'status': user_data.values_list()[0][12],
                                'mobile_number': user_data.values_list()[0][5],
                                'attempts': user_data.values_list()[0][13],
                                'approval': user_data.values_list()[0][14]})
        if request.method == 'POST':
            email_add_to_use = user_data.values_list()[0][3]
            name = request.POST['name']
            employee_id = user_data.values_list()[0][2]
            email_id = request.POST['email_id']
            try:
                status = request.POST['status']
                status = True
            except Exception as e:
                status = False
            mobile_number = request.POST['mobile_number']
            # attempts = request.POST['attempts']

            try:
                validate_email(email_id)
            except ValidationError as e:
                return render(request, 'administrative/adduser.html', {'name': request.user.username, 'form': adduser, 'errmsg': 'Email address invalid'})
            else:
                print("good email")
            updating_table = users.objects.filter(employee_id=employee_id).update(
                name=name,
                email_id=email_id,
                # status=status,
                mobile_number=mobile_number,
                # attempts=attempts
            )
            return render(request, 'administrative/editpage.html', {'employee_id': employee_id,
                                                                    'user_data': user_data,
                                                                    'form': form,
                                                                    'msg': 'Form is updated successfully.',
                                                                    'email_add_to_use': email_add_to_use})

        else:
            return render(request, 'administrative/editpage.html', {
                'employee_id': employee_id,
                'user_data': user_data,
                'form': form,
                'email_add_to_use': email_add_to_use
            })
    else:
        return redirect('/administrative/')


def delete(request, employee_id):
    if request.user.is_authenticated:
        user_data = users.objects.filter(employee_id=employee_id)
        print(user_data)

        # user_data = users.objects.filter(employee_id=employee_id).delete()

        if request.method == 'POST':
            user_data = users.objects.filter(employee_id=employee_id).delete()
            return redirect('/administrative/dashboard')
        else:
            return render(request, 'administrative/deletepage.html', {
                'employee_id': employee_id, 'user_data': user_data
            })
    else:
        return redirect('/administrative/')


def unblockuser(request, email_add_to_use):
    print('coming to unblock user')
    print(email_add_to_use)
    users.objects.filter(email_id=email_add_to_use).update(
        status=True, attempts=0)
    return redirect('dashboard')


def view(request, employee_id):
    if request.user.is_authenticated:
        user_data = users.objects.filter(employee_id=employee_id)
        print(user_data)
        return render(request, 'administrative/viewpage.html', {
            'employee_id': employee_id, 'user_data': user_data
        })
    else:
        return redirect('/administrative/')


def dashboard(request):
    if request.user.is_authenticated:
        db = users.objects.all().order_by('employee_id')
        paginator = Paginator(db, per_page=5)
        page_number = request.GET.get('page', 1)
        print(page_number)
        page_obj = paginator.get_page(page_number)
        return render(request, 'administrative/admindashboard.html', {'name': request.user.username, 'paginator': paginator, 'db': db, 'page_number': page_number})
    else:
        return redirect('/administrative/')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'administrative/logout page.html')
    else:
        return redirect('/administrative/')


def add_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['name']
            employee_id = request.POST['employee_id']
            email_id = request.POST['email_id']

            password = request.POST['password']
            # to encrypt
            # -------------- pbkdf2_sha256.encrypt(password, rounds=30000, salt_size=64)
            encrypted_password = pbkdf2_sha256.encrypt(
                password, rounds=30000, salt_size=32)
            # to verify
            # -------------- pbkdf2_sha256.verify('Newyork@123',encrypted_password)
            try:
                status = request.POST['status']
                status = True
            except Exception as e:
                status = False
            mobile_number = request.POST['mobile_number']
            attempts = request.POST['attempts']

            try:
                validate_email(email_id)
            except ValidationError as e:
                return render(request, 'administrative/adduser.html', {'name': request.user.username, 'form': adduser, 'errmsg': 'Email address invalid'})
            else:
                print("good email")
            print(name, employee_id, email_id, password,
                  status, mobile_number, attempts)
            exists_check = users.objects.filter(
                Q(employee_id=employee_id) | Q(email_id=email_id))
            if exists_check:
                return render(request, 'administrative/adduser.html', {'name': request.user.username, 'form': adduser, 'exists_error': 'Email Id or Employee id already exists cannot create user,delete it before adding...'})
            else:
                addusertodb = users.objects.create(name=name,
                                                   employee_id=employee_id,
                                                   password=encrypted_password,
                                                   email_id=email_id,
                                                   status=status,
                                                   mobile_number=mobile_number,
                                                   attempts=attempts)
                addusertodb.save()
                return render(request, 'administrative/adduser.html', {'name': request.user.username, 'form': adduser, 'msg': 'User is successfully added to database'})
        else:
            return render(request, 'administrative/adduser.html', {'name': request.user.username, 'form': adduser})

    else:
        return redirect('/administrative/')


def creategroup(request):
    if request.user.is_authenticated:
        all_members = mail_members.objects.all()
        if request.method == 'POST':
            group_name = request.POST.get('groupname')
            checking_group_name = groups.objects.filter(group_name=group_name)
            if checking_group_name:
                return render(request, 'administrative/creategroup.html', {'all_members': all_members, 'errmsg': f'{group_name} already exists'})
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
            return render(request, 'administrative/creategroup.html', {'all_members': all_members, 'msg': 'Group Created Successfully...'})

        else:
            return render(request, 'administrative/creategroup.html', {
                'all_members': all_members
            })
    else:
        return redirect('/administrative/')


def addmember(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            industry_name = request.POST.get('industry_name')
            insert_to_db = mail_members.objects.create(name=name,
                                                       email_address=email,
                                                       phone_number=phone_number,
                                                       industry_name=industry_name)
            insert_to_db.save()
            return render(request, 'administrative/addmember.html', {'msg': 'Email address is saved successfully...'})
        else:
            return render(request, 'administrative/addmember.html', {})
    else:
        return redirect('/administrative/')


def activateuser(request, email_address):
    print('activating user')
    print("---------------------------",email_address,"--------------------------------")
    user = users.objects.filter(email_id=email_address)
    print(user)
    print(email_address)
    print(request.method)
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        print(employee_id)
        department = request.POST.get("department")
        print(department)
        users.objects.filter(email_id=email_address).update(approval=True,
                                                            employee_id=employee_id,
                                                            department=department)
        print('approved...')
        return redirect('/administrative/approveuser')
    else:
        return render(request, 'administrative/viewdetails.html', {"user": user, 'email_address': email_address})


def viewdetails(request, email_address):
    user = users.objects.filter(email_id=email_address)
    print(user)
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        print(employee_id)
        department = request.POST.get("department")
        print(department)
        users.objects.filter(email_id=email_address).update(approval=True,
                                                            employee_id=employee_id,
                                                            department=department)
        print('approved...')
        return redirect('/administrative/approveuser')
    else:
        return render(request, 'administrative/viewdetails.html', {"user": user, 'email_address': email_address})
