#---------------------------------------------------------
# Import modules
#---------------------------------------------------------


#Importation des modules de manage des requetes
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404


#Importation of models
from company.models import Company, QRCode

#Importation of forms
from django import forms
from company_manager.forms import PrintQRCodesForm, OnlineOrdersForm

#transaction :
from django.db import transaction, IntegrityError

#Importation of manager user packages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from functionalities import make_many_same_qr_pdf

#Exceptions:
from django.core.exceptions import ObjectDoesNotExist

#messages :
from django.contrib import messages

import os
from django.conf import settings

#Import decorators
from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

#Online orders : Send Mail
from django.core.mail import send_mail
from django.conf import settings

#languages
from django.utils.translation import gettext as _

#QR-Codes
from functionalities import get_qrCode
#---------------------------------------------------------
# Views : Tables
#---------------------------------------------------------
#   View that allow the user to create/manage the tables
#   He can't add/or remove tables
#   But he can print the QRCode of the tables
#   Add later : Button that desactivate one table or alls the tables
#
#---------------------------------------------------------

@verified_email_required
@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def manage_qrcodes_view(request):
    """
    View with forms that ask how many QRCodes the Company want
    """

    context = {}
    current_user = request.user

    iCompany = get_object_or_404(Company,id=current_user.company_id)
    if request.method == 'POST':
        formPrintQRCodes = PrintQRCodesForm(request.POST) #Add many tables
        formOrderQRCodes = OnlineOrdersForm(request.POST)
        company_code = iCompany.company_code
        if formPrintQRCodes.is_valid():
            nbr_of_qrcodes = formPrintQRCodes.cleaned_data["nbr_of_qrcodes"]
            link = make_many_same_qr_pdf(nbr_of_qrcodes,company_code)
            #file_path = os.path.join(settings.MEDIA_ROOT, link)
            if os.path.exists(link):
                with open(link, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(link)
                    print('link :',link)
                    return response
            raise Http404
        if formOrderQRCodes.is_valid():
            if formOrderQRCodes.cleaned_data['number_for_choice1'] != 0 and formOrderQRCodes.cleaned_data['number_for_choice1'] != 0 :
                mail_message = "DEVIS DEMANDE PAR : \n \
                NOM : {} \n \
                PRENOM : {} \n \
                MAIL : {} \n \
                NOM Entreprise : {} \n \
                LIVRAISON : \n \
                Addresse : {} , {}\n \
                Code Postal : {}  \n \
                Customisation de QRCode : {} \n \
                Nombre de stickers : {} \n \
                Nombre de présentoirs  : {} \n \
                Description : {} \n \ ".format(
                    #personnals data
                    formOrderQRCodes.cleaned_data['first_name'],
                    formOrderQRCodes.cleaned_data['last_name'],
                    current_user.email,
                    iCompany.name,

                    # Shipping Details
                    formOrderQRCodes.cleaned_data['address1'],
                    formOrderQRCodes.cleaned_data['city'],
                    formOrderQRCodes.cleaned_data['zip_code'],


                    # Order Details
                    formOrderQRCodes.cleaned_data['custom_QRCodes'],
                    formOrderQRCodes.cleaned_data['number_for_choice1'],
                    formOrderQRCodes.cleaned_data['number_for_choice2'],
                    formOrderQRCodes.cleaned_data['description'],

                )
                send_mail(
                    '[DEVIS] : {}'.format(iCompany.name),
                    mail_message,
                    settings.EMAIL_HOST_USER,
                    [settings.SERVER_EMAIL],
                    fail_silently=False,
                )
                orderQRCodes = formOrderQRCodes.save(commit=False)
                orderQRCodes.company = iCompany
                orderQRCodes.save()
                messages.success(request, _('Votre demande a été transmise.'))
            else :
                messages.warning(request,_('Veuillez entrer un nombre de stickers/cartes.'))


    else :
        formPrintQRCodes = PrintQRCodesForm()
        formOrderQRCodes = OnlineOrdersForm(initial={'first_name':current_user.first_name,
                'last_name' : current_user.last_name,
                'address1' :iCompany.address1,
                'city' :iCompany.city,
                'zip_code' : iCompany.zip_code,

        })

    qrcode = get_qrCode(iCompany)
    context['company'] = iCompany
    context['qrcode'] = QRCode.objects.get(company_id=iCompany.id)
    context['formPrintQRCodes'] = formPrintQRCodes
    context['formOrderQRCodes'] = formOrderQRCodes
    return render(request, 'company/manageQrcodes.html',context)
