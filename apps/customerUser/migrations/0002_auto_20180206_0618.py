# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-06 06:18
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customerUser', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='business_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='business_name',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default=b'1390000000', help_text='In case you lost you password', max_length=128, verbose_name='Phone number'),
        ),
    ]
