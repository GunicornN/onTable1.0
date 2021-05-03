from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

#Import models
from company.models import OnlineOrders

#Import form
from company_manager.forms import AdvertisementForm

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
def manage_online_orders_view(request):
    """
    View to see all online orders
    """
    context = {}

    onlineOrders = OnlineOrders.objects.all()

    context['onlineOrders'] = onlineOrders
    return render(request, 'company/manage_online_orders.html',context)

@login_required(login_url="account_login")
@allowed_users(allowed_roles=["administratorGroup"])
def delete_online_orders(request,online_order_id):
    try:
        with transaction.atomic():
            onlineOrders = OnlineOrders.objects.get(id=online_order_id)
            onlineOrders.delete()
        messages.info(request, "La commande a bien été supprimée.")
    except ObjectDoesNotExist:
        messages.error(request, 'Une erreur est survenue.')
    return redirect('CSOnlineOrders')
