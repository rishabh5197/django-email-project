from django.shortcuts import render
from mails.models import *
from email import message
from django.conf import settings
from pytz import timezone
from celery import shared_task
from datetime import timedelta
from businessmail import settings
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail, EmailMultiAlternatives
from email.mime.image import MIMEImage
from django_celery_beat.models import PeriodicTask
from datetime import datetime
import os
from django.db.models import Q


@shared_task(bind=True,)
def schedulemail(self):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M")
    storing_args = schedulemails.objects.filter(date=date, time=time).values_list(
        'by', 'to', 'bcc', 'cc', 'subject', 'describe', 'attachments', 'session_user')
    print(storing_args)

    for i in storing_args:
        print(i)

    if storing_args:
        print('there exists values')
        by = list(storing_args)[0][0]
        to = list(storing_args)[0][1]
        cc = list(storing_args)[0][2]
        bcc = list(storing_args)[0][3]
        subject = list(storing_args)[0][4]
        description = list(storing_args)[0][5]
        attachment = list(storing_args)[0][6]
        session_user = list(storing_args)[0][7]
        try:
            mails.objects.create(title=subject,
                                 describe=description,
                                 attachments=attachment,
                                 extension=((attachment.name).split(".")[-1]).lower())
        except Exception as e:
            mails.objects.create(title=subject,
                                 describe=description,
                                 attachments=attachment)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d %B, %Y")
        sent_mails.objects.create(by=session_user,
                                  to=to,
                                  cc=cc,
                                  bcc=bcc,
                                  subject=subject,
                                  describe=description,
                                  attachments=attachment,
                                  time=current_time,
                                  date=current_date,
                                  status=False)
        print('----------------------- okay till line 53 --------------------------------')
        print('----------------------- sent_mails object working fine --------------------------------')
        print([x for x in to.replace("'", '').replace("[", "").replace("]", '').replace(
            " ", '').split(',') if x != "''"])
        print([x for x in cc.replace("'", '').replace("[", "").replace("]", '').replace(
            " ", '').split(',') if x != "''"])
        print([x for x in bcc.replace("'", '').replace("[", "").replace("]", '').replace(
            " ", '').split(',') if x != "''"])
        email = EmailMultiAlternatives(subject=subject,
                                       body=description,
                                       from_email=settings.EMAIL_HOST_USER,
                                       to=[x for x in to.replace("'", '').replace("[", "").replace("]", '').replace(
                                           " ", '').split(',') if x != "''"],
                                       cc=[x for x in cc.replace("'", '').replace("[", "").replace("]", '').replace(
                                           " ", '').split(',') if x != "''"],
                                       bcc=[x for x in bcc.replace("'", '').replace("[", "").replace(
                                           "]", '').replace(" ", '').split(',') if x != "''"]
                                       )
        print('----------------------- okay till line 56 --------------------------------')
        print('----------------------- EmailMultiAlternatives working fine --------------------------------')
        if attachment:
            print(settings.MEDIA_ROOT)
            attach = ((settings.MEDIA_ROOT).replace(
                '\\', '/')+"/"+attachment.split('/')[0])
            # attach = os.walk()
            print('Path to folder :- ', attach)
            print('File Name :- ', attachment.split('/')[1])
            try:
                with open(attach+'/'+attachment.split('/')[1], 'rb') as f:
                    # img_data = attach+'/'+attachment.split('/')[1].read()
                    img_data = f.read()
                print('file is selected....')
                # mime_image = MIMEImage(attachment.split('/')[1], name=os.path.basename(attach))
                mime_image = MIMEImage(img_data, name=os.path.basename(attach))
                print('Uploading Image')
                # (person.upload.file.name)
                # mime_image.add_header('Content-ID', '<image>')
                email.attach(mime_image)
                print('Image file attached.....')
            except Exception as e:
                print("checking for documents....")
                # email.attach(attach.name,
                #              attach.read(),
                #              attach.content_type)
                email.attach(attach)
                #          settings.MEDIA_ROOT.replace(
                # '\\', '/')+'/'+attachment.content_type)
        #         else:
        #             return render(request, 'mails/sendemail.html', {'msg': 'not a valid type of file, file must be .jpg,.png,.pdf,.bmp,.ico,.gif or .jpeg,', 'form': form, 'json_data': json_data})
        print('----------------------- Attaching file working --------------------------------')
        print('-----------------------  till line 70 okay --------------------------------')
        email.attach_alternative(description, "text/html")
        email.send()
        sent_mails.objects.filter(by=session_user,
                                  subject=subject,
                                  time=current_time,
                                  date=current_date,).update(status=True)
        print('----------------------- Sending Email done -------------------------')
        print('----------------------- line 73 okay -------------------------')
    else:
        print('there does not exists values')
        print('calling schedulemail ************************************************************',)
        print('printing args -----------------------==============------------------==========')
    # print(to, cc, bcc, title, description, attachment)


@shared_task(bind=True,)
def dailymails(self):
    date = datetime.now().strftime('%Y-%m-%d')    # today's date
    date_comparison = datetime.now()
    print(date)
    storing_args = dailymailsdatabase.objects.filter(Q(end_date__gt=date) | Q(end_date=date)).values_list(
        'by', 'to', 'bcc', 'cc', 'subject', 'describe', 'attachments', 'session_user', 'start_date', 'end_date', 'status')
    print('printing from daily task......')
    print(storing_args)

    for i in storing_args:
        print(i)

    for i in range(len(storing_args)):
        print('there exists values')
        by = list(storing_args)[i][0]
        to = list(storing_args)[i][1]
        cc = list(storing_args)[i][2]
        bcc = list(storing_args)[i][3]
        subject = list(storing_args)[i][4]
        description = list(storing_args)[i][5]
        attachment = list(storing_args)[i][6]
        session_user = list(storing_args)[i][7]
        start_date = list(storing_args)[i][8]
        end_date = list(storing_args)[i][9]
        status = list(storing_args)[i][10]
        print(by, to, cc, bcc, subject, description, attachment,
              session_user, start_date, end_date, status)
        end_date_compare = datetime.strptime(end_date, '%Y-%m-%d')
        start_date_compare = datetime.strptime(start_date, '%Y-%m-%d')
        if (end_date_compare > date_comparison) and (start_date_compare < date_comparison):
            print(start_date, end_date, date_comparison)
            email = EmailMultiAlternatives(subject=subject,
                                           body=description,
                                           from_email=settings.EMAIL_HOST_USER,
                                           to=[x for x in to.replace("'", '').replace("[", "").replace("]", '').replace(
                                               " ", '').split(',') if x != "''"],
                                           cc=[x for x in cc.replace("'", '').replace("[", "").replace("]", '').replace(
                                               " ", '').split(',') if x != "''"],
                                           bcc=[x for x in bcc.replace("'", '').replace("[", "").replace(
                                               "]", '').replace(" ", '').split(',') if x != "''"]
                                           )
            print(
                '----------------------- okay till line 159 --------------------------------')
            print(
                '----------------------- EmailMultiAlternatives working fine --------------------------------')
            if attachment:
                print(settings.MEDIA_ROOT)
                attach = ((settings.MEDIA_ROOT).replace(
                    '\\', '/')+"/"+attachment.split('/')[0])
                # attach = os.walk()
                print('Path to folder :- ', attach)
                print('File Name :- ', attachment.split('/')[1])
                try:
                    with open(attach+'/'+attachment.split('/')[1], 'rb') as f:
                        # img_data = attach+'/'+attachment.split('/')[1].read()
                        img_data = f.read()
                    print('file is selected....')
                    # mime_image = MIMEImage(attachment.split('/')[1], name=os.path.basename(attach))
                    mime_image = MIMEImage(
                        img_data, name=os.path.basename(attach))
                    print('Uploading Image')
                    # (person.upload.file.name)
                    # mime_image.add_header('Content-ID', '<image>')
                    email.attach(mime_image)
                    print('Image file attached.....')
                except Exception as e:
                    print("checking for documents....")
                    # email.attach(attach.name,
                    #              attach.read(),
                    #              attach.content_type)
                    email.attach(attach)
                    #          settings.MEDIA_ROOT.replace(
                    # '\\', '/')+'/'+attachment.content_type)
                #         else:
                #             return render(request, 'mails/sendemail.html', {'msg': 'not a valid type of file, file must be .jpg,.png,.pdf,.bmp,.ico,.gif or .jpeg,', 'form': form, 'json_data': json_data})
            print(
                '----------------------- Attaching file working --------------------------------')
            print(
                '-----------------------  till line 191 okay --------------------------------')
            email.attach_alternative(description, "text/html")
            email.send()
            print('----------------------- Sending Email done -------------------------')
            print('----------------------- line 195 okay -------------------------')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d %B, %Y")
            sent_mails.objects.create(by=session_user,
                                      to=to,
                                      cc=cc,
                                      bcc=bcc,
                                      subject=subject,
                                      describe=description,
                                      attachments=attachment,
                                      time=current_time,
                                      date=current_date,
                                      status=False)
            try:
                mails.objects.create(title=subject,
                                     describe=description,
                                     attachments=attachment,
                                     extension=((attachment.name).split(".")[-1]).lower())
            except Exception as e:
                mails.objects.create(title=subject,
                                     describe=description,
                                     attachments=attachment)
        else:
            print('Getting Passed')
            dailymailsdatabase.objects.filter(subject=subject,
                                              start_date=start_date,
                                              end_date=end_date).update(status=False)
            print('Status updated to false...')


@shared_task(bind=True,)
def weekmails(self):
    date = datetime.now().strftime('%Y-%m-%d')    # today's date
    # getting today's date in proper datetime format...
    date_comparison = datetime.now()
    print(date)

    # Filtering data from the database i.e from dailymailsdatabase.
    storing_args = weeklymailsdatabase.objects.filter(Q(end_date__gt=date) | Q(end_date=date)).values_list(
        'by', 'to', 'bcc', 'cc', 'subject', 'describe', 'attachments', 'session_user', 'start_date', 'end_date', 'status')
    print('printing from weekly task......')
    print(storing_args)
    for i in storing_args:
        print(i)

    for i in range(len(storing_args)):
        print('there exists values')
        by = list(storing_args)[i][0]
        to = list(storing_args)[i][1]
        cc = list(storing_args)[i][2]
        bcc = list(storing_args)[i][3]
        subject = list(storing_args)[i][4]
        description = list(storing_args)[i][5]
        attachment = list(storing_args)[i][6]
        session_user = list(storing_args)[i][7]
        start_date = list(storing_args)[i][8]
        end_date = list(storing_args)[i][9]
        status = list(storing_args)[i][10]
        print(by, to, cc, bcc, subject, description, attachment,
              session_user, start_date, end_date, status)
        end_date_compare = datetime.strptime(end_date, '%Y-%m-%d')
        start_date_compare = datetime.strptime(start_date, '%Y-%m-%d')
        if (end_date_compare > date_comparison) and (start_date_compare < date_comparison):
            print(start_date, end_date, date_comparison)
            email = EmailMultiAlternatives(subject=subject,
                                           body=description,
                                           from_email=settings.EMAIL_HOST_USER,
                                           to=[x for x in to.replace("'", '').replace("[", "").replace("]", '').replace(
                                               " ", '').split(',') if x != "''"],
                                           cc=[x for x in cc.replace("'", '').replace("[", "").replace("]", '').replace(
                                               " ", '').split(',') if x != "''"],
                                           bcc=[x for x in bcc.replace("'", '').replace("[", "").replace(
                                               "]", '').replace(" ", '').split(',') if x != "''"]
                                           )
            print(
                '----------------------- okay till line 248 --------------------------------')
            print(
                '----------------------- EmailMultiAlternatives working fine --------------------------------')
            if attachment:
                print(settings.MEDIA_ROOT)
                attach = ((settings.MEDIA_ROOT).replace(
                    '\\', '/')+"/"+attachment.split('/')[0])
                # attach = os.walk()
                print('Path to folder :- ', attach)
                print('File Name :- ', attachment.split('/')[1])
                try:
                    with open(attach+'/'+attachment.split('/')[1], 'rb') as f:
                        # img_data = attach+'/'+attachment.split('/')[1].read()
                        img_data = f.read()
                    print('file is selected....')
                    # mime_image = MIMEImage(attachment.split('/')[1], name=os.path.basename(attach))
                    mime_image = MIMEImage(
                        img_data, name=os.path.basename(attach))
                    print('Uploading Image')
                    # (person.upload.file.name)
                    # mime_image.add_header('Content-ID', '<image>')
                    email.attach(mime_image)
                    print('Image file attached.....')
                except Exception as e:
                    print("checking for documents....")
                    # email.attach(attach.name,
                    #              attach.read(),
                    #              attach.content_type)
                    email.attach(attach)
                    #          settings.MEDIA_ROOT.replace(
                    # '\\', '/')+'/'+attachment.content_type)
                #         else:
                #             return render(request, 'mails/sendemail.html', {'msg': 'not a valid type of file, file must be .jpg,.png,.pdf,.bmp,.ico,.gif or .jpeg,', 'form': form, 'json_data': json_data})
            print(
                '----------------------- Attaching file working --------------------------------')
            print(
                '-----------------------  till line 283 okay --------------------------------')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d %B, %Y")
            sent_mails.objects.create(by=session_user,
                                      to=to,
                                      cc=cc,
                                      bcc=bcc,
                                      subject=subject,
                                      describe=description,
                                      attachments=attachment,
                                      time=current_time,
                                      date=current_date,
                                      status=True)
            try:
                mails.objects.create(title=subject,
                                     describe=description,
                                     attachments=attachment,
                                     extension=((attachment.name).split(".")[-1]).lower())
            except Exception as e:
                mails.objects.create(title=subject,
                                     describe=description,
                                     attachments=attachment)
            email.attach_alternative(description, "text/html")
            email.send()
            print('----------------------- Sending Email done -------------------------')
            print('----------------------- line 288 okay -------------------------')

        else:
            print('Getting Passed')
            weeklymailsdatabase.objects.filter(subject=subject,
                                               start_date=start_date,
                                               end_date=end_date).update(status=False)
            print('Status updated to false...')


@shared_task(bind=True,)
def monthmails(self):
    # presentmonth = datetime.now().strftime('%Y-%m-%d')    # present month
    # getting today's date in proper datetime format...
    month_for_comparison = datetime.now().month
    print(month_for_comparison)

    # Filtering data from the database i.e from dailymailsdatabase.
    print('firing query')
    storing_args = monthlymailsdatabase.objects.filter(Q(startmonth__lte=month_for_comparison) | Q(endmonth__gte=month_for_comparison)).values_list(
        'by', 'to', 'bcc', 'cc', 'subject', 'describe', 'attachments', 'session_user', 'startmonth', 'endmonth', 'dayofmonth', 'status')
    print(storing_args)

    for i in storing_args:
        print(i)

    for i in range(len(storing_args)):
        print('there exists values')
        by = list(storing_args)[i][0]
        to = list(storing_args)[i][1]
        cc = list(storing_args)[i][2]
        bcc = list(storing_args)[i][3]
        subject = list(storing_args)[i][4]
        description = list(storing_args)[i][5]
        attachment = list(storing_args)[i][6]
        session_user = list(storing_args)[i][7]
        startmonth = list(storing_args)[i][8]
        endmonth = list(storing_args)[i][9]
        dayofmonth = list(storing_args)[i][10]
        status = list(storing_args)[i][11]
        print(by, to, cc, bcc, subject, description, attachment,
              session_user, startmonth, endmonth, status)
        # end_date_compare = datetime.strptime(endmonth, '%m')
        end_date_compare = int(endmonth)
        # start_date_compare = datetime.strptime(startmonth, '%m')
        start_date_compare = int(startmonth)
        if (end_date_compare > month_for_comparison) and (start_date_compare < month_for_comparison):
            print(startmonth, endmonth, month_for_comparison)
            email = EmailMultiAlternatives(subject=subject,
                                           body=description,
                                           from_email=settings.EMAIL_HOST_USER,
                                           to=[x for x in to.replace("'", '').replace("[", "").replace("]", '').replace(
                                               " ", '').split(',') if x != "''"],
                                           cc=[x for x in cc.replace("'", '').replace("[", "").replace("]", '').replace(
                                               " ", '').split(',') if x != "''"],
                                           bcc=[x for x in bcc.replace("'", '').replace("[", "").replace(
                                               "]", '').replace(" ", '').split(',') if x != "''"]
                                           )
            print(
                '----------------------- okay till line 352 --------------------------------')
            print(
                '----------------------- EmailMultiAlternatives working fine --------------------------------')
            if attachment:
                print(settings.MEDIA_ROOT)
                attach = ((settings.MEDIA_ROOT).replace(
                    '\\', '/')+"/"+attachment.split('/')[0])
                # attach = os.walk()
                print('Path to folder :- ', attach)
                print('File Name :- ', attachment.split('/')[1])
                try:
                    with open(attach+'/'+attachment.split('/')[1], 'rb') as f:
                        # img_data = attach+'/'+attachment.split('/')[1].read()
                        img_data = f.read()
                    print('file is selected....')
                    # mime_image = MIMEImage(attachment.split('/')[1], name=os.path.basename(attach))
                    mime_image = MIMEImage(
                        img_data, name=os.path.basename(attach))
                    print('Uploading Image')
                    # (person.upload.file.name)
                    # mime_image.add_header('Content-ID', '<image>')
                    email.attach(mime_image)
                    print('Image file attached.....')
                except Exception as e:
                    print("checking for documents....")
                    # email.attach(attach.name,
                    #              attach.read(),
                    #              attach.content_type)
                    email.attach(attach)
                    #          settings.MEDIA_ROOT.replace(
                    # '\\', '/')+'/'+attachment.content_type)
                #         else:
                #             return render(request, 'mails/sendemail.html', {'msg': 'not a valid type of file, file must be .jpg,.png,.pdf,.bmp,.ico,.gif or .jpeg,', 'form': form, 'json_data': json_data})
            print(
                '----------------------- Attaching file working --------------------------------')
            print(
                '-----------------------  till line 388 okay --------------------------------')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%d %B, %Y")
            sent_mails.objects.create(by=session_user,
                                      to=to,
                                      cc=cc,
                                      bcc=bcc,
                                      subject=subject,
                                      describe=description,
                                      attachments=attachment,
                                      time=current_time,
                                      date=current_date,
                                      status=True)
            try:
                mails.objects.create(title=subject,
                                     describe=description,
                                     attachments=attachment,
                                     extension=((attachment.name).split(".")[-1]).lower())
            except Exception as e:
                mails.objects.create(title=subject,
                                     describe=description,
                                     attachments=attachment)
            email.attach_alternative(description, "text/html")
            email.send()
            print('----------------------- Sending Email done -------------------------')
            print('----------------------- line 392 okay -------------------------')
            # now = datetime.now()
            # current_time = now.strftime("%H:%M:%S")
            # current_date = now.strftime("%d %B, %Y")
            # sent_mails.objects.create(by=session_user,
            #                           to=to,
            #                           cc=cc,
            #                           bcc=bcc,
            #                           subject=subject,
            #                           describe=description,
            #                           attachments=attachment,
            #                           time=current_time,
            #                           date=current_date)
            # mails.objects.create(title=subject,
            #                      describe=description,
            #                      attachments=attachment,
            #                      extension=((attachment.name).split(".")[-1]).lower())
        else:
            print('Getting Passed')
            monthlymailsdatabase.objects.filter(subject=subject,
                                                startmonth=startmonth,
                                                endmonth=endmonth).update(status=False)
            print('Status updated to false...')

# @shared_task(bind=True)
# def send_mail_func(self):
#     users = group_members().objects.all()
#     #timezone.localtime(users.date_time) + timedelta(days=2)
#     for user in users:
#         mail_subject =
#         message = "If you are liking my content, please hit the like button and do subscribe to my channel"
#         to_email = user.email
#         send_mail(
#             subject=mail_subject,
#             message=message,
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[to_email],
#             fail_silently=True,
#         )
#     return "Done"
