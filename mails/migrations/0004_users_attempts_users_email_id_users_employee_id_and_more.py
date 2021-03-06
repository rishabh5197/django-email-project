# Generated by Django 4.0.1 on 2022-01-17 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_users_alter_mails_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='users',
            name='email_id',
            field=models.EmailField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='employee_id',
            field=models.CharField(default='A-', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='mobile_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
