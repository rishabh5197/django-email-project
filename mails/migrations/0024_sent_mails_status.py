# Generated by Django 3.2.11 on 2022-02-17 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0023_users_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='sent_mails',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
