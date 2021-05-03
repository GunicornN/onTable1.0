from django.contrib import admin
from .models import CustomUser

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.models import User


#admin.site.unregister(User)
admin.site.register(User,CustomUser)