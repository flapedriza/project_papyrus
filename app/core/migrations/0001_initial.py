# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-14 02:04
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
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=16)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=16)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Date updated')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('expiration_date', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
                ('tags', models.ManyToManyField(to='core.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
