from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

#Import forms
from company_manager.forms import DocumentForm

#Import models
from company.models import Company, Customer

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#Import decorators
from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

#Import transactions and errors
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

#Import packages for users
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.translation import gettext as _

@verified_email_required
@login_required(login_url="account_login")
def manage_customer_infos_view(request):
    """
    View with forms that ask how many QRCodes the Company want
    """
    context = {}
    current_user = request.user
    current_company = get_object_or_404(Company,id=current_user.company_id)
    customer_infos = Customer.objects.filter(company=current_company)

    context['customer_infos'] = customer_infos
    #context['current_company'] = current_company
    return render(request, 'company/customer_infos.html',context)


@verified_email_required
@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def delete_customer_infos(request,customer_id):
    try:
        with transaction.atomic():
            customer_infos = Customer.objects.get(id=customer_id)
            customer_infos.delete()
        messages.info(request, _("Customer information has been deleted."))
    except ObjectDoesNotExist:
        messages.error(request, _('An error occurred.'))
    return redirect('CSCustomersInfos')
