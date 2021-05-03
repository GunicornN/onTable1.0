#---------------------------------------------------------
# Importation des modules
#---------------------------------------------------------


#Importation des modules de manage des requetes
from django.shortcuts import render, redirect
from django.http import HttpResponse


#Importation des modèles
from company.models import *
from company.models import Company

#Importation des formulaires
from django import forms
from company_manager.forms import *

#Importation des modules de manage des Utilisateurs
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Exceptions:
from django.core.exceptions import ObjectDoesNotExist

#Import decorators
from company_manager.decorators import profil_completed, allowed_users
#---------------------------------------------------------
# View : Payment
#---------------------------------------------------------



@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def payment_view(request):
    context = {}



    return render(request, 'company/payment.html',context)


@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def payment_accepted_view(request):
    context = {}



    return render(request, 'company/paymentAccepted.html',context)
