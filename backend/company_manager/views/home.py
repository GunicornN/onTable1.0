#---------------------------------------------------------
# Imports
#---------------------------------------------------------

from django.shortcuts import render, redirect
from django.http import HttpResponse

from company.models import Company, QRCode

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

from functionalities import get_qrCode
from django.core.mail import send_mail

#---------------------------------------------------------
# View : Home
#---------------------------------------------------------

@verified_email_required
@login_required(login_url="account_login")
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

    try :
        qrcode = get_qrCode(iCompany)
        context['qrcode'] = qrcode
    except FileNotFoundError:
        context['qrcode'] = None 
    
    context['company'] = iCompany
    return render(request, 'company/home.html',context)
