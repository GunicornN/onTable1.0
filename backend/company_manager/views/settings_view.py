#---------------------------------------------------------
# Imports
#---------------------------------------------------------


#Import packages for requests
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.http import HttpResponse

#Imports of forms
from company_manager.forms import SettingsCompanyForm

#Import packages for users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from company.models import Company
from core.models import CustomUser

#Import transactions and errors
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

#Import decorators
from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

from django.utils.translation import gettext as _

#---------------------------------------------------------
# View : Settings
#---------------------------------------------------------

@verified_email_required
@login_required(login_url="account_login")
def settings_view(request):
    context = {}
    current_user = request.user

    if request.method == "POST":  
        formSettingsCompany = SettingsCompanyForm(request.POST)
        if not current_user.hasCompany():
             #the company exist so we change values based of forms inputs
            if formSettingsCompany.is_valid():
                formSettingsCompany.save()
            elif formSettingsCompany.is_valid():
                    # The compagny doesn't  exist so we create one
                    with transaction.atomic():
                        company = formSettingsCompany.save(commit=False)
                        company.user = request.user
                        company.save()

                        company.set_company_code()

                        current_user.company = company
                        current_user.save()
                        current_user.setGroup()

        messages.success(request, _('Your settings have been saved.'))

    else :
        try:
            company = Company.objects.get(id=current_user.company_id)
            context['company'] = company
            formSettingsCompany = SettingsCompanyForm(
            initial={'name':company.name,
                    'address1' : company.address1,
                    'address2' :company.address2,
                    'city' :company.city,
                    'zip_code' : company.zip_code,

                        }
                    )
        except ObjectDoesNotExist :
            formSettingsCompany = SettingsCompanyForm(
            initial={'name':'',
                    'address1' : '',
                    'address2' : '',
                    'city' :'',
                    'zip_code' : '',
                        }
                    )


    context['formSettingsCompany'] = formSettingsCompany
    return render(request, 'company/settings.html',context)


@login_required(login_url="account_login")
@verified_email_required
def delete_account_view(request):
    if request.method == "POST":
        current_user = request.user
        try:
            company = Company.objects.get(id=current_user.company_id)
            company.delete()
        except ObjectDoesNotExist :
            pass
        with transaction.atomic():
            try:
                user = CustomUser.objects.get(id=current_user.id)
                user.delete()
            except ObjectDoesNotExist :
                pass

    return redirect('homePage')
