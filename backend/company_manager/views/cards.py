#---------------------------------------------------------
# Imports
#---------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from company.models import Company, Categories, Cards, Products

from django import forms
from django.forms import modelformset_factory
from company_manager.forms.cards_forms import CategoriesFormset, ProductsFormset, addFormulasOrCardsForm

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from company_manager.decorators import profil_completed, allowed_users

from django.utils.translation import gettext as _

#---------------------------------------------------------
# View : Cards
#---------------------------------------------------------



@profil_completed
@login_required(login_url="account_login")
def add_products_view(request):

    context = {}
    current_user = request.user


    if request.method == 'POST':
        productsFormset = ProductsFormset(request.POST)

    else :
        productsFormset = ProductsFormset()

    context['productsFormset'] = productsFormset

    return render(request, 'company/addProducts.html',context)

# View that create a card
@profil_completed
@login_required(login_url="account_login")
def add_products_to_card_category_view(request,cardSlug,categorySlug):

    current_user = request.user
    card = get_object_or_404(Cards, Company_id=current_user.company_id,slug=cardSlug)
    category = get_object_or_404(Categories,Company_id=current_user.company_id,slug=categorySlug)

    context = {}



    if request.method == 'POST':
        formset1 = ProductsFormset(request.POST)

    else :
        formset1 = ProductsFormset()


    context['formset1'] = formset1
    context['formset2'] = formset2
    return render(request, 'company/addProductsToCardCategory.html',context)

@profil_completed
@login_required(login_url="account_login")
def add_categories_to_card_view(request,cardSlug):
    """
    This view will add categories to the a specific card

    """

    current_user = request.user

    card = get_object_or_404(Cards,company_id=current_user.company_id,slug=cardSlug)
    lsCategories = Categories.objects.filter(company_id=current_user.company_id,slug=cardSlug)
    context = {}

    if request.method == 'POST':
        categoriesFormset = CategoriesFormset(request.POST)
    else :
        categoriesFormset = CategoriesFormset()

    context['categoriesFormset'] = categoriesFormset
    context['lsCategories'] = lsCategories
    context['card'] = card
    return render(request, 'company/addCategoriesToCard.html',context)

@profil_completed
@login_required(login_url="account_login")
def add_formulas_or_cards_view(request):
    context = {}
    current_user = request.user
    current_company = Company.objects.get(id=current_user.company_id)

    lsCardsAndFormulas = Cards.objects.filter(company_id=current_user.company_id)
    if request.method == 'POST':
        addFormulasOrCards = addFormulasOrCardsForm(request.POST)
        if addFormulasOrCards.is_valid():

            if addFormulasOrCards.cleaned_data['typeOfCreation'] == '2':
                cardName = addFormulasOrCards.cleaned_data['name']
                try:
                    #test if a card exist
                    card = Cards.objects.get(name=cardName,id=current_user.company_id)
                    messages.info(request, _('A card with the same name already exists.'))
                except ObjectDoesNotExist :
                    with transaction.atomic():
                        CardName = Cards.objects.get_or_create(
                            name=cardName,
                            company=current_company,
                            description=addFormulasOrCards.cleaned_data['description']
                            )

                    messages.info(request, _('Your card has been created.'))
    else :
        addFormulasOrCards = addFormulasOrCardsForm()

    context['lsCardsAndFormulas'] = lsCardsAndFormulas
    context['addFormulasOrCards'] = addFormulasOrCards
    return render(request, 'company/addFormulasOrCards.html',context)
