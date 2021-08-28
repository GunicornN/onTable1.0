from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

#Import forms
from company_manager.forms import PictureCardForm

#Import models
from company.models import Company, pictureCard

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

from django.conf import settings

from django.utils.translation import gettext as _


@verified_email_required
@login_required(login_url="account_login")
def model_form_upload(request):
    context = {}
    current_user = request.user
    current_company = get_object_or_404(Company,id=current_user.company_id)

    lsDocument = pictureCard.objects.get_cards_from_company(current_company)
    if request.method == 'POST':
        form = PictureCardForm(request.POST, request.FILES)
        if len(lsDocument)  >= settings.MAX_DOCUMENTS_PER_ACCOUNT:
            messages.info(request, _('Your account file limit is {}').format(settings.MAX_DOCUMENTS_PER_ACCOUNT))
        elif form.is_valid():
            file = form.cleaned_data['picture']
            if pictureCard.objects.filter(name=form.cleaned_data['name'],company=current_company).exists():
                messages.info(request, _('You have already uploaded a document with the same name.'))
            else :
                if int(file.size) > settings.MAX_UPLOAD_SIZE:
                    messages.info(request, _("Maximum file size is 10MB."))
                else :
                    # If the document doesn't exist, respect the max size, then create this new document
                    with transaction.atomic():
                        form.save(company=current_company,upload_by=current_company.name,)
                        messages.success(request, _('Your document is being added.'))
    else:
        form = PictureCardForm()

    lsDocument = pictureCard.objects.get_cards_from_company(current_company)
    context['lsDocument'] = lsDocument
    context['form'] = form
    context['MAX_DOCUMENTS_PER_ACCOUNT'] = settings.MAX_DOCUMENTS_PER_ACCOUNT
    context['lenDocument'] = len(lsDocument)
    return render(request, 'company/upload.html',context)


@verified_email_required
@login_required(login_url="account_login")
def delete_upload(request,document_name):
    current_user = request.user
    current_company = get_object_or_404(Company,id=current_user.company_id)
    try:
        with transaction.atomic():
            pictures = pictureCard.objects.get_images_from_company_card(company=current_company,card_name=document_name)
            for picture in pictures :
                picture.delete()
        messages.info(request, _("Document deleted successfully."))
    except ObjectDoesNotExist:
        messages.error(request, _('An error occurred.'))
    return redirect('CSUploadDocument')


@verified_email_required
@login_required(login_url="account_login")
def view_document(request,document_name):
    context = {}
    current_user = request.user

    current_company = get_object_or_404(Company,id=current_user.company_id)
    cards_images = pictureCard.objects.get_images_from_company_card(company=current_company,card_name=document_name)

    context['company']  = current_company
    context['document_name']  = document_name
    context['cards_images']  = cards_images
    return render(request, 'company/seeDocument.html',context)