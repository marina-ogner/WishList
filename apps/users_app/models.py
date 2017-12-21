# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from datetime import datetime as dt
from django.db import models
from ..login_registration_app.models import User


# Create your models here.

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "No empty entries"
            return errors
        if len(postData['name']) < 3:
            errors['name'] = "Item should be more than 3 characters"
            return errors
        

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="created_item")
    joiner = models.ManyToManyField(User, related_name="joined_item")
    objects = BlogManager()
    def __repr__(self):
        return "<Item: {}, creator: {}, joiner: {}>".format(self.name, self.creator, self.joiner)
