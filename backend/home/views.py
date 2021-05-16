from django.shortcuts import render, get_object_or_404, redirect
from company.models import Company, pictureCard
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, get_language,
)

#Import forms
from company_manager.forms import PictureCardFormset

#languages
from django.utils.translation import gettext as _

def homePage_view(request):
    context = {}
    nb_company = Company.objects.filter().count()
    context['nb_company'] = nb_company
    return render(request, "home/index.html", context)

def searchCompany(request):
    # https://docs.djangoproject.com/en/dev/topics/db/queries/#complex-lookups-with-q-objects/
    # search_companies 
    context = {}
    if request.method == 'POST' and request.POST['iSearchCompany'] != '' :
        search = request.POST['iSearchCompany']
        companies = Company.objects.filter(Q(name__contains=search) | 
                                        Q(company_code__contains=search) |
                                        Q(address1__contains=search) |
                                        Q(address2__contains=search) |
                                        Q(city__contains=search))
                                        
        
        if companies.count() == 1 :
            return redirect("companyPresentation",pk=companies[0].id)
        elif not companies:
            context['error'] = "No Company Found"
        else:
            context['search'] = search
            context['companies'] = companies
        return render(request,'home/companies_search.html',context)
    else :
        return render(request,'home/companies_search.html',context)
#----------------------------------------------------------------------------
# MAYBE REMOVE THIS 
#----------------------------------------------------------------------------
def addCardToCompany(request,company_id):

    company = get_object_or_404(Company,id=pk)
    #Check if there are documents imported by the Restaurant
    company_documents = pictureCard.objects.get_cards_from_company(company=company)
    if not company_documents and company_documents[0].upload_by == 'company':
        messages.info(request, _("Vous ne pouvez pas ajouter de documents."))

    if request.method == 'POST':
        file = form.cleaned_data['document']
        file_name = file.name
        if file_name.endswith('.png'):
            try:
                test_file = Document.objects.get(name=form.cleaned_data['name'],company=company)
                messages.info(request, _('Vous avez déjà envoyé un document avec le même nom.'))
            except Document.DoesNotExist :
                print(file.size)
                if int(file.size) > settings.MAX_UPLOAD_SIZE:
                    messages.info(request, _("La taille maximum est de 10MB."))
                else :
                    with transaction.atomic():
                        document_to_upload = form.save(commit=False)
                        document_to_upload.company = company
                        document_to_upload.upload_by = 'unknown'
                        document_to_upload.save()
                        messages.success(request, _('Votre PDF a bien été rajouté.'))
                        #need to add doc to img models 
#----------------------------------------------------------------------------
# END REMOVE THIS 
#----------------------------------------------------------------------------

def company_presentation_view(request,pk):
    context = {}
    current_company = get_object_or_404(Company,id=pk)

    company_pictureCard = pictureCard.objects.get_cards_from_company(company=current_company).exclude(upload_by='unknown')

    #test if the company have not upload documents 
    if not company_pictureCard:
        
        if request.method == 'POST':
            cardName = request.POST['name']
            pictureCard_formset = PictureCardFormset(request.POST)
            if pictureCard_formset.is_valid() and cardName != '':
                for form in pictureCard_formset:
                    if form.is_valid():
                        form = form.save(company=current_company,upload_by='unknown',cardName=cardName)
        else :
            pictureCard_formset = PictureCardFormset()
        
        context['pictureCard_formset'] = pictureCard_formset      

    
    context['company'] = current_company
    return render(request,"home/company_presentation.html",context)

def CGU_view(request):
    return render(request, "home/CGU.html", {})

def privacy_policy_view(request):
    return render(request, "home/privacy_policy.html", {})

def view_404(request,exception):
    return render(request,'home/errors/404.html')

def view_500(request):
    return render(request,'home/errors/500.html')
