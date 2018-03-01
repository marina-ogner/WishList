
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
import random

from django.contrib import messages
from .models import User

def login_validator(request):
    result = User.objects.login_validator(request.POST)
    if type(result)==dict:
        for tag, error in result.iteritems():
            messages.error(request, error, extra_tags=tag) # or just error(request, message, extra_tags=field)
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        request.session['first_name'] = result.first_name
        return redirect('/dashboard')

def registration_validator(request):
    result = User.objects.registration_validator(request.POST)
    if type(result) == dict:
        for tag, error in result.iteritems():
            messages.error(request, error, extra_tags=tag) # or just error(request, message, extra_tags=field)
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        request.session['first_name'] = result.first_name
        messages.success(request, "Successfully registered!")
        return redirect('/dashboard')

def index(request):
    context = {
        "key":"value"
    }
    return render(request, 'login_registration_app/index.html', context)

def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/main')


