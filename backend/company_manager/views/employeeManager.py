#---------------------------------------------------------
# Import modules
#---------------------------------------------------------


#Import packages to manage requests
from django.shortcuts import render, redirect
from django.http import HttpResponse

#Importation of manager user packages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#Import messages
from django.contrib import messages

#Import company model
from company.models import Company
from company_manager.forms import AddEmployeeForm

#Import users model
from users.models import CustomUser, EmployeeRequest

#Import decorators
from company_manager.decorators import profil_completed, allowed_users
from allauth.account.decorators import verified_email_required

#Import transactions and errors
from django.db import transaction

#Import errors
from django.core.exceptions import ObjectDoesNotExist

#languages
from django.utils.translation import gettext as _
#---------------------------------------------------------
# Views : Waiters
#---------------------------------------------------------
#   View that allow the user to create/manage the employee, allowing
#   them to access the company manager
#---------------------------------------------------------
#   Test if the email input is in the BDD :
#   If No : Send  an e-mail to the waiter
#   If Yes : Add the waiter to the Company
#

@verified_email_required
@login_required(login_url="account_logout")
@profil_completed
@allowed_users(allowed_roles=["companyGroup"])
def employee_manager_view(request):
    context = {}

    user_exist = False
    current_user = request.user
    current_company = Company.objects.get(id=current_user.company_id)

    if request.method == "POST" :
        formAddEmployee = AddEmployeeForm(request.POST)
        for buttons in request.POST :
            #Add an Employee
            if buttons.startswith("addAnEmployee"):
                for buttons in request.POST :
                    if formAddEmployee.is_valid():
                        email = formAddEmployee.cleaned_data['employeeEmail']
                        try:
                            toUser = CustomUser.objects.get(email=email)
                            user_exist = True
                            if user_exist and not toUser.company_id :
                                with transaction.atomic():
                                    company = Company.objects.get(id=current_user.company_id)
                                    frequest, created = EmployeeRequest.objects.get_or_create(
                            			from_user=company,
                            			to_user=toUser)
                                    messages.success(request, _('Une demande a été envoyée à votre employé.'))
                            elif toUser.company_id == current_user.company_id and toUser == current_user :
                                messages.info(request, _('Vous ne pouvez pas vous envoyer des invitations.'))
                            elif toUser.groups.filter(name='companyGroup').exists():
                                messages.info(request, _('Cette personne possède un compte entreprise.'))
                                messages.info(request, _('Vous ne pouvez ajouter que des comptes employés.'))
                            else :
                                messages.info(request, 'Cette personne a déjà une entreprise.')
                            #Rajouter des messages : Si une invitation a déjà été envoyée

                        except ObjectDoesNotExist :
                            messages.error(request,_("Aucun employé n'est associé à cet email."))

            #Remove an Employee
            if buttons.startswith("button-remove-id"):
                idEmployee = int(buttons.rsplit('_', 1)[1])
                try:
                    with transaction.atomic():
                        employee = CustomUser.objects.get(id=idEmployee)
                        employee.company_id = None
                        employee.save()
                    messages.info(request, _("L'Employé a bien été supprimé."))
                except ObjectDoesNotExist:
                    messages.error(request, _('Une erreur est survenue.'))

            #Remove an Invitation
            if buttons.startswith("button-cancel-id"):
                mailEmployee = str(buttons.rsplit('_', 1)[1])
                try:
                    with transaction.atomic():
                        employee = CustomUser.objects.get(email=mailEmployee)
                        request = EmployeeRequest.objects.get(to_user=employee.id,from_user=current_user.id).delete()
                    messages.info(request, _("L'Employé a bien été supprimé."))
                except ObjectDoesNotExist:
                    messages.error(request, _('Une erreur est survenue.'))


    elif user_exist == False or request.method == "GET" :
        formAddEmployee = AddEmployeeForm()

    #List of employee working for the company
    try:
        lsEmployeeWorkingForTheCompany = CustomUser.objects.filter(groups__name='employeeGroup',company_id=current_company.id)
    except Exception as e:
        lsEmployeeWorkingForTheCompany = []

    lsOfInvitationsThatSentTheCompany = EmployeeRequest.objects.filter(from_user=current_company)

    #lsOfInvitationsThatSentTheCompany = []

    context['lsOfInvitationsThatSentTheCompany'] = lsOfInvitationsThatSentTheCompany
    context['lsEmployeeWorkingForTheCompany'] = lsEmployeeWorkingForTheCompany
    context['AddEmployeeForm'] = AddEmployeeForm
    return render(request, 'company/employeeManager.html',context)
