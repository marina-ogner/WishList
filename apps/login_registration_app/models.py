# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from datetime import datetime as dt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# Create your models here.

class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        if len(self.filter(username=post_data['username'])) > 0: # or User.objects.filter
            # check this user's password
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['username_password'] ='!!! Username/password incorrect'
        else:
            errors['username_password'] ='!!! Username/password incorrect'

        if errors:
            return errors
        return user

    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['date_hired']) < 1:
            errors["date_hired"] = "!!! Date Hired cannot be empty"
        else: 
            today = datetime.now().strftime("%Y-%m-%d")
            date_hired = datetime.strptime(str(post_data["date_hired"]),'%Y-%m-%d').strftime("%Y-%m-%d") 
            if date_hired > today:
                errors["date_hired2"] = "!!! Date hired should be less than today"
        if len(post_data['first_name']) < 3:
            errors["first_name"] = "!!! First name should be at least 3 characters"
        if len(post_data['username']) < 3:
            errors["username"] = "!!! User name should be at least 3 characters"
        if len(post_data['password']) < 8:
            errors["password"] = "!!! Password should be more than 7 characters"
        if re.search('[A-Za-z]', post_data['password']) is None:
            errors["password"] = "!!! Password must have at least characters"  
        # if not re.match(NAME_REGEX, post_data['password']):
        #     errors['password'] = "!!! Password should be at least characters" 
        if not "email" in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "!!! Invalid email"
        if post_data['password'] != post_data['password_confirm']:
            errors["password"] = "!!! Passwords do not match"
        if len(User.objects.filter(email=post_data['email'])) > 0:  # or 1 when use get, not filter
            errors['email'] = "!!! Email already in use"
        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                first_name=post_data['first_name'],
                username=post_data['username'],
                email=post_data['email'],
                password=hashed,
                date_hired=datetime.strptime(str(post_data["date_hired"]),'%Y-%m-%d')
            )
            return new_user
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return self.email