# Generated by Django 2.0.13 on 2019-06-04 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0004_auto_20190603_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
