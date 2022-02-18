# Generated by Django 4.0.1 on 2022-01-22 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0007_alter_users_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='mail_members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='demo', max_length=100)),
                ('email_address', models.EmailField(default='demo@gmail.com', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='attempts',
            field=models.IntegerField(default=0, help_text='Nos of attempts made by failure'),
        ),
        migrations.AlterField(
            model_name='users',
            name='email_id',
            field=models.EmailField(help_text='Email id assigned to employee', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='employee_id',
            field=models.CharField(default='', help_text='Employee Id assigned to employee', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='mobile_number',
            field=models.CharField(help_text='Mobile Number of Employee', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(help_text='Name of employee', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(help_text='Password of employee', max_length=200, null=True),
        ),
    ]