from django.shortcuts import render, redirect, get_object_or_404

from .forms import ConnexionForm, CustomerInfosForm

from django.http import HttpResponseRedirect

#exceptions
from django.db import transaction

#messages
from django.contrib import messages

#celery tasks
from company_manager.tasks import convert_from_company_pdf, convert_and_check_company_pdf

# models 
from company.models import Company, pictureCard, Advertisement, Customer, Product

def CustomerInfo(request,company_code):
    company = get_object_or_404(Company, company_code=company_code)
    if request.method == 'POST' :
        customer_infos_form = CustomerInfosForm(request.POST)
        if customer_infos_form.is_valid():
            with transaction.atomic():
                customer_infos_form = customer_infos_form.save(commit=False)
                customer_infos_form.company = company
                customer_infos_form.save()
                messages.success(request, 'Thank you for your information.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def company_home(request,company_code):
    #WRITE THIS AGAIN
    context = {}
    company = get_object_or_404(Company, company_code=company_code)
    ls_cards = pictureCard.objects.get_cards_from_company(company)
    ls_ads = Advertisement.objects.filter(companies__id=company.id)

    current_ad = company.current_ad

    if ls_ads and len(ls_ads) >= 1  :
        if not current_ad + 1 >= len(ls_ads):
            current_ad += 1
        else :
            current_ad = 0
        company.current_ad = current_ad
        company.save()
        # TODO: optimize this query
        ad = get_object_or_404(Advertisement,companies__id=company.id,id=ls_ads[current_ad].id)
        context['ad']  = ad
        ad.view += 1
        ad.save()

    context['customer_infos_form'] = CustomerInfosForm()
    context['company'] = company
    context['ls_cards'] =ls_cards
    return render(request, 'orders/home.html',context)

# TO DO
def order_online(request,slug):
    context = {}
    company = get_object_or_404(Company,slug=slug)
    products = Product.objects.filter(company=company)

    context['company'] = company
    context['products'] = products
    
    print(products)
    return render(request,'orders/order_online.html',context)

# DEBUGING 
def debug_404(request,slug):
    context = {}
    company = get_object_or_404(Company,slug=slug)
    products = Product.objects.filter(company=company)

    context['company'] = company
    context['products'] = products
    return render(request,'orders/order_online.html',context)

def company_cards(request,company_code,document_name):
    context = {}

    company = get_object_or_404(Company,company_code=company_code)
    cards_images = pictureCard.objects.get_images_from_company_card(company=company,card_name=document_name)

    if 'images' in cards_images[0].picture.name:
        images_media_files =  True
    else : 
        images_media_files = False
    """
    if not images_from_pdf:
        convert_from_company_pdf.delay(document.name,company.company_code)
    else :
        convert_and_check_company_pdf.delay(document.name,company.company_code,len(images_from_pdf))
    """
    
    context['images_media_files']  = images_media_files
    context['company']  = company
    context['customer_infos_form'] = CustomerInfosForm()
    context['cards_images']  = cards_images
    return render(request, 'orders/cards.html',context)

def connexion_view(request):
    if request.method == "POST":
        form_connexion = ConnexionForm(request.POST)
        if form_connexion.is_valid():
            get_company_code = form_connexion.cleaned_data['code_connexion'][:4]
            company = get_object_or_404(Company, company_code=get_company_code)
            return redirect('OSHome',company_code=get_company_code)
    else :
        form_connexion = ConnexionForm()

    return render(request, 'orders/connexion.html',{'form_connexion':form_connexion,
    })

def view_404(request,exception):
    return render(request,'orders/errors/404.html')

def view_500(request):
    return render(request,'orders/errors/500.html')
