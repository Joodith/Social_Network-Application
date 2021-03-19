# Generated by Django 3.1.7 on 2021-03-14 06:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0006_auto_20210314_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 6, 20, 24, 873865, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='pic',
            field=models.ImageField(upload_to='posts/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 14, 6, 20, 24, 872867, tzinfo=utc)),
        ),
    ]
