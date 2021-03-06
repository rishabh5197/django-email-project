import array
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
import random


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
                # employee_id = "E - "+str(int(users.objects.latest('id').id)+1)
                employee_id = users.objects.filter(
                    email_id=email_id).values(employee_id)
                print("------ Employee id is ------ :- ", employee_id)
                addusertodb = users.objects.create(name=name,
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
    print("---------------------------", email_address,
          "--------------------------------")
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


def strong_password():
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12

    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                         'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                         'Z']

    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
               '*', '(', ')', '<']

    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
        password = password + x

    # print out password
    print(password)
    return password


def viewdetails(request, email_address):
    print("ID :-", int(users.objects.latest('id').id)+1)
    user = users.objects.filter(email_id=email_address)
    print(user)
    if request.method == "POST":
        # employee_id = request.POST.get("employee_id")

        # -------------- this is yet to resolve --------------------

        # employee_id = "E -"+str(user.objects.filter())

        # -------------- this is yet to resolve --------------------
        # print(employee_id)
        department = request.POST.get("department")
        print(department)
        # users.objects.filter(email_id=email_address).update(approval=True,
        #                                                     employee_id=employee_id,
        #                                                     department=department)

        print('approved....')
        password = strong_password()
        print(password)
        send_mail('Password for your account',
                  f'Here is your temporary password {password} to log in to your account',
                  settings.EMAIL_HOST_USER,
                  [email_address],
                  fail_silently=False,)
        encrypted_password = pbkdf2_sha256.encrypt(
            password, rounds=30000, salt_size=32)
        users.objects.filter(email_id=email_address).update(approval=True,
                                                            department=department,
                                                            on_creation_password=encrypted_password)
        print("email sent")
        return redirect('/administrative/dashboard')
    else:
        return render(request, 'administrative/viewdetails.html', {"user": user, 'email_address': email_address})


def createcompanygroup(request):
    if request.user.is_authenticated:
        print(request.method)
        if 'creategroup' in request.GET:
            print('creategroup' in request.GET)
            group_name = request.GET.get("group_name")
            print(group_name)
            if users_group.objects.filter(group_name=group_name):
                return render(request, 'administrative/createcompanygroup.html', {'errmsg': 'Group already exists'})
            else:
                all_user = users.objects.all().order_by('employee_id')
                return render(request, 'administrative/createcompanygroup.html', {'all_user': all_user, 'group_name': group_name})
        elif 'clickedcreategroup' in request.GET:
            group_name = request.GET.get("group_name")
            listofemails = request.GET.getlist("check")
            if listofemails:
                print(listofemails)
                for i in listofemails:
                    print(i)
                    aa = users_group.objects.create(email_id=i,
                                                    group_name=group_name)
                    aa.save()
                return render(request, 'administrative/createcompanygroup.html', {'goodmsg': 'group created..'})
            else:
                all_user = users.objects.all().order_by('employee_id')
                return render(request, 'administrative/createcompanygroup.html', {'all_user': all_user, 'group_name': group_name, 'errmsg': 'please select one or more members.'})
        else:
            pass
        return render(request, 'administrative/createcompanygroup.html', )
    else:
        return redirect('/administrative/')


def viewcompanygroup(request):
    all_groups = users_group.objects.all().values('group_name').distinct()
    print(all_groups)
    if all_groups:
        print(True)
    else:
        print(False)
    return render(request, 'administrative/viewcompanygroup.html', {"all_groups": all_groups})


def groupname(request, group_name):
    print(group_name)
    all_users = users_group.objects.filter(group_name=group_name)
    print(all_users)
    return render(request, 'administrative/companygroupmember.html', {'group_name': group_name, 'all_users': all_users})


def deletecompanymember(request, email_id, group_name):
    users_group.objects.filter(
        group_name=group_name, email_id=email_id).delete()
    print("deleted")
    return redirect(f"/administrative/viewcompanygroup/{group_name}")


def addcompanygroupmembers(request, group_name):
    if request.user.is_authenticated:
        all_members = [x['email_id'] for x in list(
            users.objects.all().values('email_id'))]
        present_users = [x['email_id'] for x in list(users_group.objects.filter(
            group_name=group_name).values('email_id'))]
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
                bb = users_group.objects.create(
                    email_id=i, group_name=group_name)
                bb.save()
            return redirect(f'/administrative/viewcompanygroup/{group_name}')

        else:
            return render(request, 'administrative/addcompanygroupmembers.html', {'group_name': group_name,
                                                                                  'users_to_be_added': users_to_be_added})
    else:
        return redirect('/administrative/addcompanygroupmembers.html')


def deletecompanygroup(request, group_name):
    print("==================", group_name)
    users_group.objects.filter(group_name=group_name).delete()
    return redirect(f"/administrative/viewcompanygroup")

# if request.method == 'POST':
#         # if request.POST.get('fetch_id'):
#         if 'fetch_id' in request.POST:
#             email_address = request.POST.get('email_address')
#             print(email_address)
#             questions = users.objects.filter(
#                 email_id=email_address).values_list('question_1', 'question_2')
#             question_1, question_2 = questions[0][0], questions[0][1]
#             return render(request, 'mails/forgetpage.html', {'email_address': email_address, 'question_1': question_1,
#                                                              'question_2': question_2})
#         # elif request.POST.get('')
#         elif 'validate_answers' in request.POST:
#             email_address = request.POST.get('email_address')
#             questions = users.objects.filter(
#                 email_id=email_address).values_list('question_1', 'question_2')
#             question_1, question_2 = questions[0][0], questions[0][1]
#             answer_1 = request.POST.get('answer_1')
#             answer_2 = request.POST.get('answer_2')
#             return render(request, 'mails/forgetpage.html', {'email_address': email_address,
#                                                              'question_1': question_1,
#                                                              'question_2': question_2,
#                                                              'answer_1': answer_1,
#                                                              'answer_2': answer_2})
#     return render(request, 'mails/forgetpage.html', {})
