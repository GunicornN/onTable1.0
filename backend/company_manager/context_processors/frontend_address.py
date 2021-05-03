from company.models import Company
from django.core.exceptions import ObjectDoesNotExist
from onTableAPI.settings.common import FRONTEND_ADDRESS

"""
This function return the name of the company, to display it into the nav bar

"""
def frontend_address(request):
    return {'frontend_address': FRONTEND_ADDRESS}

