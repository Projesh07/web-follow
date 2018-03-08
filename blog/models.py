# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    followerUser=models.ForeignKey(User, related_name='followerUser')
    followeeUser=models.ForeignKey(User, related_name='followeeUser')

    def __unicode__(self):
        return 'id=' + str(self.id)

class Item(models.Model):
    bio = models.TextField()
    picture = models.FileField(upload_to="images", blank=True)
    content_type = models.CharField(max_length=50)
    toUser=models.ForeignKey(User, related_name='thisUser')

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'



class PostEntry(models.Model):
    last_name       = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=20)
    post_content  = models.CharField(max_length=200)
    post_time       = models.DateTimeField()
    post_user = models.ForeignKey(User, related_name='postUser')

    def __unicode__(self):
        return 'Entryid=' + str(self.id) + ',text="' + self.post_content + '"'

class CommentEntry(models.Model):
    last_name       = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=20)
    comment_content  = models.CharField(max_length=200)
    comment_time       = models.DateTimeField()
    comment_user = models.ForeignKey(User)
    toPost = models.ForeignKey(PostEntry, related_name='comments')

    def __unicode__(self):
        return self.text
