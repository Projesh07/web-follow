# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-20 05:35
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
            name='CommentEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('comment_content', models.CharField(max_length=200)),
                ('comment_time', models.DateTimeField()),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followeeUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followeeUser', to=settings.AUTH_USER_MODEL)),
                ('followerUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followerUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('picture', models.FileField(blank=True, upload_to='images')),
                ('content_type', models.CharField(max_length=50)),
                ('toUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thisUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('post_content', models.CharField(max_length=200)),
                ('post_time', models.DateTimeField()),
                ('post_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commententry',
            name='toPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.PostEntry'),
        ),
    ]
