# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-22 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feature_requests', '0002_auto_20181222_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='SinglePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=40)),
                ('postcode', models.CharField(blank=True, max_length=15)),
                ('town_or_city', models.CharField(max_length=30)),
                ('street_address1', models.CharField(max_length=40)),
                ('street_address2', models.CharField(max_length=40)),
                ('county', models.CharField(blank=True, max_length=30)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SinglePaymentLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feature_requests.FeatureRequest')),
                ('single_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.SinglePayment')),
            ],
        ),
    ]
