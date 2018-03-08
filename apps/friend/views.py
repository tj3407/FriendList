# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import md5

# Create your views here.
def index(req):
    return redirect('/main')

def main(req):
    if 'user_id' in req.session:
        return redirect('/friends')
    return render(req, 'friend/index.html')

#POST - handle registration request
def register(req):
    errors = User.objects.basic_validator(req.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/')
    else:
        get_user = User.objects.filter(email=req.POST['email'])
        if get_user.exists():
            email = get_user[0].email
            if req.POST['email'] == email:
                messages.error(req, "Email is already taken")
                return redirect('/')
        else:
            user = User.objects.create(name=req.POST['name'], alias=req.POST['alias'], email=req.POST['email'], dob=req.POST['dob'], password=md5.new(req.POST['password']).hexdigest())
            req.session["user_id"] = user.id
            req.session['alias'] = req.POST['alias']
            return redirect('/friends')

#POST - handle login request
def login(req):
    user = User.objects.filter(email=req.POST['email'])
    if user:
        current_user = user[0]
        if current_user.password == md5.new(req.POST['password']).hexdigest():
            req.session['user_id'] = current_user.id
            req.session['alias'] = current_user.alias
            return redirect('/friends')
    messages.error(req, "No email and password combo found")
    return redirect('/main')

#GET - logout from session
def logout(req):
    del req.session['user_id']
    del req.session['alias']
    return redirect("/")

#GET - retrieve user and friends list
def friends(req):
    if 'user_id' not in req.session:
        return redirect('/')
    else:
        context = {
            "users": User.objects.all().exclude(id=req.session['user_id']).exclude(user__in=Friend.objects.filter(user=User.objects.get(id=req.session['user_id']))),
            "friends": Friend.objects.filter(user=User.objects.get(id=req.session['user_id']))
        }
        return render(req, 'friend/friends.html', context)

#GET - add user to friends list
def join(req, id):
    Friend.objects.create(user=User.objects.get(id=req.session['user_id']), friend=User.objects.get(id=id))
    Friend.objects.create(user=User.objects.get(id=id), friend=User.objects.get(id=req.session['user_id']))
    return redirect('/')

#GET - remove user from friends list
def remove(req, id):
    Friend.objects.get(user=User.objects.get(id=req.session['user_id']), friend=User.objects.get(id=id)).delete()
    Friend.objects.get(user=User.objects.get(id=id), friend=User.objects.get(id=req.session['user_id'])).delete()
    return redirect('/')

#GET - show user profile
def profile(req, id):
    context = {
        "user": User.objects.get(id=id)
    }
    return render(req, 'friend/profile.html', context)