
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import datetime
from django.db.models import Q
import random
from django.contrib import messages
from .models import * 
# Create your views here.


def index(request):
    context = {
            "personal_items" : Item.objects.filter(creator = User.objects.get(id=request.session['user_id']))|Item.objects.filter(joiner = User.objects.get(id=request.session['user_id'])),
            "other_items" : Item.objects.all().exclude(Q(creator = User.objects.get(id=request.session['user_id']))|Q(joiner = User.objects.get(id=request.session['user_id']))),
        }

    # print request.session['user_id']
    return render(request, 'users_app/users.html', context)

def clear(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/main')

def add(request):
    return render(request, 'users_app/add.html')

def create(request):
    errors = Item.objects.basic_validator(request.POST)
    if type(errors)==dict:
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/wish_items/create')
    else:
        u1 = User.objects.get(id=request.session['user_id'])
        i1 = Item(name = request.POST["name"], creator = u1)
        i1.save()
        return redirect('/wish_items')
        

def join(request, item_id):
    u1 = User.objects.get(id=request.session['user_id'])
    i1 = Item.objects.get(id=item_id)
    i1.joiner.add(u1)
    return redirect('/wish_items')

def delete(request, item_id):
    i1 = Item.objects.get(id=item_id)
    i1.delete()
    return redirect('/wish_items')

def delete_from_list(request, item_id):
    i1 = Item.objects.get(id=item_id)
    u1 = User.objects.get(id=request.session['user_id'])
    i1.joiner.remove(u1)
    return redirect('/wish_items')

def about_item(request, item_id):
    al = Item.objects.get(id=item_id).joiner.all()
    # print al
    me = Item.objects.get(id=item_id).joiner.filter(id=request.session['user_id'])
    # print me
    result = al.difference(me)

    context = {
        "about_item" : Item.objects.get(id=item_id),
        "other_users" : result,
    }
    return render(request, 'users_app/about_item.html', context)




#Trip.objects.all().joiner.values()
