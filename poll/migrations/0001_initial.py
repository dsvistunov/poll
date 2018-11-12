# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-12 13:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anonymous',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=120)),
                ('votes', models.IntegerField(default=0)),
                ('max_value', models.IntegerField(blank=True, null=True)),
                ('min_value', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('TXT', 'text'), ('RAD', 'radio'), ('CHK', 'checkbox'), ('SLT', 'select'), ('MSL', 'multiselect'), ('NUM', 'number'), ('EMP', '')], default='EMP', max_length=3, verbose_name='Answer type')),
                ('size', models.IntegerField(default=1)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Poll')),
                ('voted_anonymous', models.ManyToManyField(to='poll.Anonymous')),
                ('voted_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.Question'),
        ),
    ]
