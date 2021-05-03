from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

#Import models
from company.models import Company

#Import decorators
from company_manager.decorators import allowed_users

#Import transactions and errors
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

#Import packages for users
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="account_login")
@allowed_users(allowed_roles=["administratorGroup"])
def administration_view(request):
    """
    View with forms that ask how many QRCodes the Company want
    """

    context = {}
    companies = Company.objects.all()

    context['companies'] = companies
    return render(request, 'company/administration.html',context)
