# Generated by Django 3.2.11 on 2022-02-15 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0021_auto_20220211_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='address',
            field=models.CharField(help_text='address', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='answer_1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='answer_2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='approval',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='department',
            field=models.CharField(help_text='Department name', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='question_1',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='question_2',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
