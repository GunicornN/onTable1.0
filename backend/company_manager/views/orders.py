#---------------------------------------------------------
# Imports
#---------------------------------------------------------


#Importation des modules de manage des requetes
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse


#Importation des modèles
from company.models import *
from company.models import Company

#Importation des formulaires
from django import forms
from company_manager.forms import *


#Exceptions:
from django.core.exceptions import ObjectDoesNotExist

#Importation des modules de manage des Utilisateurs
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Import decorators
from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

#Get time
from datetime import datetime

from django.core import serializers
#
#---------------------------------------------------------
# View : Orders
#---------------------------------------------------------
#These functions are used to see current orders. Your job
#is to create them. Following the manual
#---------------------------------------------------------


@verified_email_required
@profil_completed
@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def orders_view(request):
    context = {}
    current_orders = {}
    current_user = request.user
    now = datetime.now()
    iCompany = get_object_or_404(Company,id=current_user.company_id)

    lsOrders = Cart.objects.filter(company_id=iCompany.id,
        createdOn__hour__range=[now.hour-1, now.hour], #Range of -1 hour
        createdOn__date = now.date(), #Current date
        ).order_by('-createdOn') #Change to updateOn

    lsTables = Tables.objects.filter(cart__in=Cart.objects.filter(
        createdOn__hour__range=[now.hour-1, now.hour], #Range of -1 hour
        createdOn__date = now.date(), #Current date
        )
    ).order_by('-updatedOn').distinct()

    data = serializers.serialize("xml", lsTables)

    context['lsOrders']  = lsOrders
    context['lsTables']  = lsTables
    context['data']  = data
    context['time']  = now.time() #We pass the time to be sure that servor and clients are synchronized
    return render(request, 'company/orders.html',context)

"""
class Orders_View(ListView):
    queryset = Tables.objects.filter(cart__in=Cart.objects.filter(
        createdOn__hour__range=[now.hour-1, now.hour], #Range of -1 hour
        createdOn__date = now.date(), #Current date
        )
    ).order_by('-updatedOn').distinct()
    template_name = 'company/orders.html'




    for x in range(len(lsTables)) :
        if lsTables[x] == lsTables[x+1]:
            pass
    for o in lsOrders:
        print(o)
        print(o.table.tableNo)
context['lsTables']  = lsTables
    for order in lsOrders :
        current_orders[tableNumber] = order.table.tableNo
        nouveauPanier
    for table in lsTables:
        for order in lsOrders:
            pass
def get_data(request,*args,**kwargs):

    iCompany = get_object_or_404(id=current_user.company_id)

    if request.method == 'GET':


    return JsonResponse()
"""
