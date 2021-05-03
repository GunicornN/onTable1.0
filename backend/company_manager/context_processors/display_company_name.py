from company.models import Company
from django.core.exceptions import ObjectDoesNotExist


"""
This function return the name of the company, to display it into the nav bar

"""
def display_company_name(request):
    try:
        if(request.user.id):
            companyName =  Company.objects.get(id=request.user.company_id).name
            return {
                'companyName': companyName
            }
    except ObjectDoesNotExist:
        pass

    return {'companyName': "Aucun"}
