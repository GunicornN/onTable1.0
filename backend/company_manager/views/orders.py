#---------------------------------------------------------
# Imports
#---------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

from company.models import Company, Cart, Table

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

from datetime import datetime

from django.core import serializers

#---------------------------------------------------------
# View : Orders
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

    lsTables = Table.objects.filter(cart__in=Cart.objects.filter(
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
