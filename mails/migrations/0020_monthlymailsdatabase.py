# Generated by Django 3.2.11 on 2022-02-09 11:06

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0019_weeklymailsdatabase'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthlymailsdatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.EmailField(max_length=1000)),
                ('to', models.CharField(max_length=10000)),
                ('bcc', models.CharField(blank=True, max_length=1000, null=True)),
                ('cc', models.CharField(blank=True, max_length=1000, null=True)),
                ('subject', models.CharField(max_length=1000)),
                ('describe', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('attachments', models.FileField(upload_to='files/')),
                ('session_user', models.EmailField(blank=True, max_length=1000, null=True)),
                ('startmonth', models.CharField(blank=True, max_length=25, null=True)),
                ('endmonth', models.CharField(blank=True, max_length=25, null=True)),
                ('dayofmonth', models.CharField(blank=True, max_length=25, null=True)),
                ('status', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]