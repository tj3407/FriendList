# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

import re, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        try:
            date = postData["dob"]
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if date > datetime.date.today():
                errors["dob"] = "Date of Birth must NOT be in the future"
        except:
            errors["dob"] = "Date of Birth must not be empty"
        if len(postData["name"]) < 3:
            errors["name"] = "Name Required; No fewer than 3 characters; letters only"
        if len(postData['alias']) < 3:
            errors["alias"] = "Alias Required; No fewer than 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email Required; Must be a valid format"
        if len(postData['password']) < 8: 
            errors["password"] = "Password Required; No fewer than 8 characters in length"
        if postData['password'] != postData['confirm']:
            errors["confirm"] = "Password must match"
        if postData['dob'] == "":
            errors["dob"] = "Date of Birth must not be empty"
        return errors

class QuoteManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["author"]) < 3:
            errors["author"] = "Quoted by should be more than 3 characters"
        if len(postData["quote"]) < 10:
            errors["quotes"] = "Message should be more than 10 characters"

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Friend(models.Model):
    user = models.ForeignKey(User, related_name="friend")
    friend = models.ForeignKey(User, related_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

