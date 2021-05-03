#---------------------------------------------------------
# Importation des modules
#---------------------------------------------------------


#Importation des modules de manage des requetes
from django.shortcuts import render, redirect
from django.http import HttpResponse


#Importation des modèles
from company.models import *
from company.models import Company, QRCode

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
from allauth.account.decorators import verified_email_required

#QR-Codes
from functionalities import get_qrCode
#---------------------------------------------------------
# View : Home
#---------------------------------------------------------
from django.core.mail import send_mail

@verified_email_required
@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def homePage_view(request):
    context = {}
    current_user = request.user
    try:
        iCompany = Company.objects.get(id=current_user.company_id)
    except ObjectDoesNotExist:
        return render(request, 'errors/noCompleted.html',context)
    #Check if profile is full completed
    if not iCompany.check_if_profil_completed():
        return render(request, 'errors/noCompleted.html',context)

    qrcode = get_qrCode(iCompany)
    context['qrcode'] = qrcode
    context['company'] = iCompany
    return render(request, 'company/home.html',context)
