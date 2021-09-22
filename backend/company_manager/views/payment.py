#---------------------------------------------------------
# Imports
#---------------------------------------------------------

from django.shortcuts import render, redirect
from django.http import HttpResponse

from company.models import Company

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

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
