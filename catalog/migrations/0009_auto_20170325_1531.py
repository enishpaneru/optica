# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-25 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20170325_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glass',
            name='name',
            field=models.CharField(max_length=25),
        ),
    ]
