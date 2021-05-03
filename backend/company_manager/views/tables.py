#---------------------------------------------------------
# Import modules
#---------------------------------------------------------


#Importation des modules de manage des requetes
from django.shortcuts import render, redirect
from django.http import HttpResponse


#Importation of models
from company.models import Company, Tables

#Importation of forms
from django import forms
from company_manager.forms import AddTableForm

#transaction :
from django.db import transaction, IntegrityError

#Importation of manager user packages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from functionalities import table_code_generator, make_1qr_pdf, make_many_qr_pdf

#Exceptions:
from django.core.exceptions import ObjectDoesNotExist

#messages :
from django.contrib import messages

#CHANGE THIS CONF
import os
from django.conf import settings
from django.http import HttpResponse, Http404

#Import decorators
from company_manager.decorators import profil_completed, allowed_users

from allauth.account.decorators import verified_email_required

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
@profil_completed
@login_required(login_url="account_login")
@allowed_users(allowed_roles=["companyGroup"])
def manage_tables_view(request):
    """
    View with forms that ask how many QRCodes the Company want
    """

    context = {}

    #Identification variables

    current_user = request.user

    iCompany = Company.objects.get(id=current_user.company_id)
    listOfTables = Tables.objects.filter(company=iCompany).order_by('tableNo')

    if request.method == 'POST':
        formAddTables = AddTableForm(request.POST) #Add many tables
        formAddTable = AddTableForm(request.POST)   #Add one table

        for buttons in request.POST :

            #Creation of many tables
            if buttons.startswith("addManyTables"):
                if formAddTables.is_valid():

                    numberOfTablesToCreate = formAddTables.cleaned_data['table_data']
                    if numberOfTablesToCreate >= 200 :
                        messages.info(request, "Il n'est pas possible d'avoir plus de 200 tables.")
                    else :
                        try:
                            lastNumberOfTable = listOfTables.last().tableNo
                        except Exception:
                            #AttributeError
                            lastNumberOfTable =  0
                        for tableNumber in range(lastNumberOfTable,lastNumberOfTable+numberOfTablesToCreate) :
                            with transaction.atomic():
                                table = Tables.objects.create(
                                    tableNo=tableNumber+1,
                                    tableCode=table_code_generator(tableNumber+1),
                                    company=iCompany
                                )

            #Creation of one table
            if buttons.startswith("addOneTable"):
                if formAddTable.is_valid():
                    tableNumber = formAddTable.cleaned_data['table_data']
                    if tableNumber >= 200 :
                        messages.info(request, "Il n'est pas possible d'avoir plus de 200 tables.")
                    else :
                        try:
                            tableNumberAlreadyExist = Tables.objects.get(tableNo=tableNumber,company=iCompany)
                            messages.error(request, 'Cette table existe déjà.')
                        except ObjectDoesNotExist:
                            #The object doesn't exist so we create one
                            with transaction.atomic():
                                table = Tables.objects.create(
                                    tableNo=tableNumber,
                                    tableCode=table_code_generator(tableNumber),
                                    company=iCompany)


            #Remove a table
            if buttons.startswith("button-remove-id_"):
                tableNumber = int(buttons.rsplit('_', 1)[1])
                try:
                    tableDelete = Tables.objects.get(tableNo=tableNumber,company=iCompany)
                    tableDelete.delete()
                except ObjectDoesNotExist:
                    messages.error(request, 'Une erreur est survenue.')

            #Print All the QRCodes
            if buttons.startswith('printAllQRCodeBtn') :
                #Check if the table exist, if no send 1 error
                try:
                    tables =  Tables.objects.filter(company=iCompany)
                except ObjectDoesNotExist:
                    #Send an error
                    #Stop
                    pass
                tablesCodes = []
                tablesNumbers = []
                for table in tables :
                    tablesCodes.append(table.tableCode)
                    tablesNumbers.append(table.tableNo)

                link = make_many_qr_pdf(tablesNumbers,iCompany.CompanyCode,tablesCodes)
                file_path = os.path.join(settings.MEDIA_ROOT, link)
                if os.path.exists(file_path):
                    with open(link, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(link)
                        return response
                raise Http404

            #Print only 1 QRCODE
            if buttons.startswith('button-print-QRCode-id') :
                tableNumber = int(buttons.rsplit('_', 1)[1])
                try:
                    table =  Tables.objects.get(tableNo=tableNumber,company=iCompany)

                except ObjectDoesNotExist:
                    messages.error(request, 'Il y a eu une erreur')
                try:
                    link = make_1qr_pdf(tableNumber,iCompany.CompanyCode,table.tableCode)
                    file_path = os.path.join(settings.MEDIA_ROOT, link)
                    if os.path.exists(file_path):
                        with open(link, 'rb') as fh:
                            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(link)
                            return response
                except Exception as e:
                    raise Http404



    else :
        formAddTables = AddTableForm()
        formAddTable = AddTableForm()

    context['listOfTables'] = listOfTables
    context['formAddTables'] = formAddTables
    context['formAddTable'] = formAddTable
    return render(request, 'company/manageTables.html',context)
