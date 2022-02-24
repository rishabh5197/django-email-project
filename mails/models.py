import email
from pydoc import describe
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import os

# Create your models here.


class mails(models.Model):
    title = models.CharField(max_length=1000)
    # describe = models.TextField()
    describe = RichTextField(blank=True, null=True)
    attachments = models.FileField(
        upload_to="files/", blank=False, null=False,)
    extension = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.title}"


class sent_mails(models.Model):
    by = models.EmailField(max_length=1000)
    to = models.CharField(max_length=1000)
    bcc = models.CharField(max_length=1000, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000)
    # describe = models.TextField()
    describe = RichTextField(blank=True, null=True)
    attachments = models.FileField(
        upload_to="files/", blank=False, null=False,)
    date = models.CharField(max_length=25, null=True, blank=True)
    time = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.by} -> {self.to} == {self.subject}"


class users(models.Model):
    name = models.CharField(max_length=100, null=True,
                            help_text='Name of employee')
    employee_id = models.CharField(
        max_length=10, default='', null=True, help_text='Employee Id assigned to employee')
    email_id = models.EmailField(
        max_length=150, null=True, help_text="Email id assigned to employee")
    password = models.CharField(
        max_length=200, null=True, help_text="Password of employee")
    mobile_number = models.CharField(
        max_length=15, null=True, help_text="Mobile Number of Employee")
    department = models.CharField(
        max_length=100, null=True, help_text='Department name')
    question_1 = models.CharField(max_length=1000, null=True)
    question_2 = models.CharField(max_length=1000, null=True)
    answer_1 = models.CharField(max_length=100, null=True)
    answer_2 = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=1000, null=True, help_text='address')
    status = models.BooleanField()
    attempts = models.IntegerField(
        default=0, help_text='Nos of attempts made by failure')
    approval = models.BooleanField(null=True)
    otp = models.CharField(max_length=10, null=True)
    group_creation = models.BooleanField(default=False, null=True)
    group_edition = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"{self.email_id}"


class groups(models.Model):
    group_name = models.CharField(max_length=100, null=True)


class mail_members(models.Model):
    name = models.CharField(max_length=100, null=False, default='demo')
    email_address = models.EmailField(
        max_length=100, null=False, default='demo@gmail.com', unique=True)
    phone_number = models.CharField(max_length=15, null=True)
    industry_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name}  --  {self.email_address}"


class group_members(models.Model):
    group_name = models.CharField(max_length=100)
    # group_members = models.ForeignKey(mail_members, on_delete=models.CASCADE)
    email_address = models.EmailField(
        max_length=100, null=True,)


class schedulemails(models.Model):
    by = models.EmailField(max_length=1000)
    to = models.CharField(max_length=10000)
    bcc = models.CharField(max_length=1000, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000)
    # describe = models.TextField()
    describe = RichTextField(blank=True, null=True)
    attachments = models.FileField(
        upload_to="files/", blank=False, null=False,)
    session_user = models.EmailField(max_length=1000, blank=True, null=True)
    date = models.CharField(max_length=25, null=True, blank=True)
    time = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return f"{self.by} -> {self.to} == {self.subject}"


class dailymailsdatabase(models.Model):
    by = models.EmailField(max_length=1000)
    to = models.CharField(max_length=10000)
    bcc = models.CharField(max_length=1000, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000)
    # describe = models.TextField()
    describe = RichTextField(blank=True, null=True)
    attachments = models.FileField(
        upload_to="files/", blank=False, null=False,)
    session_user = models.EmailField(max_length=1000, blank=True, null=True)
    start_date = models.CharField(max_length=25, null=True, blank=True)
    end_date = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f"{self.by} -> {self.to} == {self.subject} from {self.start_date} to {self.end_date}"


class weeklymailsdatabase(models.Model):
    by = models.EmailField(max_length=1000)
    to = models.CharField(max_length=10000)
    bcc = models.CharField(max_length=1000, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000)
    # describe = models.TextField()
    describe = RichTextField(blank=True, null=True)
    attachments = models.FileField(
        upload_to="files/", blank=False, null=False,)
    session_user = models.EmailField(max_length=1000, blank=True, null=True)
    start_date = models.CharField(max_length=25, null=True, blank=True)
    end_date = models.CharField(max_length=25, null=True, blank=True)
    day = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.by} -> {self.to} == {self.subject} from {self.start_date} to {self.end_date}"


class monthlymailsdatabase(models.Model):
    by = models.EmailField(max_length=1000)
    to = models.CharField(max_length=10000)
    bcc = models.CharField(max_length=1000, blank=True, null=True)
    cc = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000)
    # describe = models.TextField()
    describe = RichTextField(blank=True, null=True)
    attachments = models.FileField(
        upload_to="files/", blank=False, null=False,)
    session_user = models.EmailField(max_length=1000, blank=True, null=True)
    startmonth = models.CharField(max_length=25, null=True, blank=True)
    endmonth = models.CharField(max_length=25, null=True, blank=True)
    dayofmonth = models.CharField(max_length=25, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.by} -> {self.to} == {self.subject} from {self.startmonth} to {self.endmonth}"
