# Generated by Django 4.0.1 on 2022-01-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0013_sent_mails'),
    ]

    operations = [
        migrations.AddField(
            model_name='sent_mails',
            name='date',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='sent_mails',
            name='time',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
