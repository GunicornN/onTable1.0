#---------------------------------------------------------
# Imports
#---------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

from company.models import Company, QRCode

from company_manager.forms import PrintQRCodesForm, OnlineOrdersForm

from django.db import transaction, IntegrityError

from django.contrib.auth.decorators import login_required

from functionalities import make_many_same_qr_pdf

from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

import os
from django.conf import settings

from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

from django.core.mail import send_mail
from django.utils.translation import gettext as _

from functionalities import get_qrCode

#---------------------------------------------------------
# Views : QR Codes
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
                mail_message = "QUOTE REQUESTED BY: \n \
                LAST NAME: {} \n \
                FIRST NAME: {} \n \
                EMAIL: {} \n \
                Company Name: {} \n \
                SHIPPING: \n \
                Address: {} , {}\n \
                Zip Code: {}  \n \
                QR Code Customization: {} \n \
                Number of stickers: {} \n \
                Number of displays: {} \n \
                Description: {} \n \ ".format(
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
                    '[QUOTE] : {}'.format(iCompany.name),
                    mail_message,
                    settings.EMAIL_HOST_USER,
                    [settings.SERVER_EMAIL],
                    fail_silently=False,
                )
                orderQRCodes = formOrderQRCodes.save(commit=False)
                orderQRCodes.company = iCompany
                orderQRCodes.save()
                messages.success(request, _('Your request has been submitted.'))
            else :
                messages.warning(request,_('Please enter a number of stickers/cards.'))


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
